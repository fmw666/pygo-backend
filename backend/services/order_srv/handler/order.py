import json
import time
import random

from common.register import consul
from common.grpc_interceptor.retry import RetryInterceptor
from order_srv.model.models import OrderGoods, OrderInfo, ShoppingCart
from order_srv.proto import (order_pb2, order_pb2_grpc, goods_pb2,
                             goods_pb2_grpc, inventory_pb2, inventory_pb2_grpc)
from order_srv.settings import settings

import grpc
from google.protobuf import empty_pb2
from loguru import logger
from peewee import DoesNotExist
from rocketmq.client import (TransactionMQProducer, TransactionStatus, Message,
                             SendStatus, Producer, ConsumeStatus)


local_execute_dict = {}


def generate_order_sn(user_id):
    """
    生成订单号
    """
    random_num = random.Random().randint(10, 99)
    return f"{time.strftime('%Y%m%d%H%M%S')}{user_id}{random_num}"


def order_timeout(msg):
    """
    订单超时回调函数
    """
    msg_body = json.loads(msg.body.decode("utf-8"))
    order_sn = msg_body["orderSn"]

    # 1. 查询订单支付状态
    with settings.DB.atomic() as txn:
        try:
            order = OrderInfo.get(OrderInfo.order_sn == order_sn)
            if order.status != "TRADE_SUCCESS":
                order.status = "TRADE_CLOSED"
                order.save()

                # 2. 给库存服务发送归还库存消息
                msg = Message("order_reback")
                msg.set_keys("pygo")
                msg.set_tags("reback")
                msg.set_body(json.dumps({"orderSn": order_sn}))

                sync_producer = Producer("order_sender")
                sync_producer.set_name_server_address(
                    f"{settings.ROCKETMQ_HOST}:{settings.ROCKETMQ_PORT}")
                sync_producer.start()
                ret = sync_producer.send_sync(msg)
                if ret.status != SendStatus.OK:
                    raise Exception("send message failed")
                sync_producer.shutdown()
        except Exception:
            txn.rollback()
            return ConsumeStatus.RECONSUME_LATER
        return ConsumeStatus.CONSUME_SUCCESS


class OrderServicer(order_pb2_grpc.OrderServicer):

    @logger.catch
    def CartItemList(self, request: order_pb2.UserInfoRequest, context):
        """
        获取用户购物车列表
        """
        items = ShoppingCart.select().where(ShoppingCart.user == request.id)
        rsp = order_pb2.CartItemListResponse(total=items.count())
        for item in items:
            rsp.data.append(order_pb2.ShopCartInfoResponse(
                id=item.id,
                userId=item.user,
                goodsId=item.goods,
                nums=item.nums,
                checked=item.checked
            ))
        return rsp

    @logger.catch
    def CreateCartItem(self, request: order_pb2.CartItemRequest, context):
        """
        添加商品到购物车
        """
        existed = ShoppingCart.select().where(
            ShoppingCart.goods == request.goodsId,
            ShoppingCart.user == request.userId
        )

        # 如果商品已经存在，则增加数量
        if existed:
            item = existed[0]
            item.nums += request.nums
        else:
            item = ShoppingCart(
                goods=request.goodsId,
                user=request.userId,
                nums=request.nums
            )
        item.save()
        return order_pb2.ShopCartInfoResponse(id=item.id)

    @logger.catch
    def UpdateCartItem(self, request: order_pb2.CartItemRequest, context):
        """
        更新购物车商品: 修改数量，选中状态
        """
        try:
            item = ShoppingCart.get(
                ShoppingCart.user == request.userId,
                ShoppingCart.goods == request.goodsId
            )
            if request.checked:
                item.checked = request.checked
            if request.nums:
                item.nums = request.nums
            item.save()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("购物车记录不存在")
        return empty_pb2.Empty()

    @logger.catch
    def DeleteCartItem(self, request: order_pb2.CartItemRequest, context):
        """
        删除购物车商品
        """
        try:
            item = ShoppingCart.get(
                ShoppingCart.user == request.userId,
                ShoppingCart.goods == request.goodsId
            )
            item.delete_instance()
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("购物车记录不存在")
        return empty_pb2.Empty()

    @logger.catch
    def OrderList(self, request: order_pb2.OrderFilterRequest, context):
        """
        获取订单列表
        """
        rsp = order_pb2.OrderListResponse()

        orders = OrderInfo.select()
        if request.userId:
            orders = orders.where(OrderInfo.user == request.userId)
        rsp.total = orders.count()

        # 分页
        page_per_nums = request.pagePerNums if request.pagePerNums else 10
        start = (request.pages - 1) * page_per_nums if request.pages > 0 else 0
        orders = orders.limit(page_per_nums).offset(start)

        for order in orders:
            rsp.data.append(order_pb2.OrderInfoResponse(
                id=order.id,
                userId=order.user,
                orderSn=order.order_sn,
                payType=order.pay_type,
                status=order.status,
                message=order.leave_message,
                total=order.order_mount,
                address=order.address,
                name=order.signer_name,
                mobile=order.signer_mobile,
                addTime=order.add_time.strftime("%Y-%m-%d %H:%M:%S"),
            ))

        return rsp

    @logger.catch
    def OrderDetail(self, request: order_pb2.OrderRequest, context):
        """
        获取订单详情
        """
        rsp = order_pb2.OrderInfoDetailResponse()

        try:
            if request.userId:
                order = OrderInfo.get(OrderInfo.id == request.id,
                                      OrderInfo.user == request.userId)
            else:
                order = OrderInfo.get(OrderInfo.id == request.id)

            rsp.orderInfo.id = order.id
            rsp.orderInfo.userId = order.user
            rsp.orderInfo.orderSn = order.order_sn
            rsp.orderInfo.payType = order.pay_type
            rsp.orderInfo.status = order.status
            rsp.orderInfo.message = order.leave_message
            rsp.orderInfo.total = order.order_mount
            rsp.orderInfo.address = order.address
            rsp.orderInfo.name = order.signer_name
            rsp.orderInfo.mobile = order.signer_mobile

            order_goods = OrderGoods.select().where(
                OrderGoods.order == order.id)
            for order_good in order_goods:
                rsp.data.append(order_pb2.OrderItemResponse(
                    goodsId=order_good.goods,
                    goodsName=order_good.goods_name,
                    goodsImage=order_good.goods_image,
                    goodsPrice=order_good.goods_price,
                    goodsNums=order_good.nums,
                ))
            return rsp
        except DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("订单不存在")
            return rsp

    @logger.catch
    def UpdateOrderStatus(self, request: order_pb2.OrderStatusRequest,
                          context):
        """
        更新订单支付状态
        """
        OrderInfo.update(status=request.status).where(
            OrderInfo.order_sn == request.orderSn).execute()
        return empty_pb2.Empty()

    @logger.catch
    def check_callback(self, msg):
        """
        RocketMQ 消费回调函数
        """
        msg_body = json.loads(msg.body.decode("utf-8"))
        order_sn = msg_body["orderSn"]

        # 查询本地数据库。查询 order_sn 订单是否存在
        orders = OrderInfo.select().where(OrderInfo.order_sn == order_sn)
        if orders:
            return TransactionStatus.ROLLBACK
        else:
            return TransactionStatus.COMMIT

    @logger.catch
    def local_execute(self, msg, user_args):
        """
        RocketMQ 本地事务执行函数
        """
        msg_body = json.loads(msg.body.decode("utf-8"))
        order_sn = msg_body["orderSn"]
        local_execute_dict[order_sn] = {}

        retry_codes = [grpc.StatusCode.UNAVAILABLE,
                       grpc.StatusCode.DEADLINE_EXCEEDED,
                       grpc.StatusCode.UNKNOWN]
        retry_interceptor = RetryInterceptor(retry_codes=retry_codes)
        with settings.DB.atomic() as txn:
            goods_ids = []
            goods_nums = {}
            order_mount = 0
            order_goods_list = []
            goods_sell_info = []
            for cart_item in ShoppingCart.select().where(
                ShoppingCart.user == msg_body["userId"],
                checked=True
            ):
                goods_ids.append(cart_item.goods)
                goods_nums[cart_item.goods] = cart_item.nums

            if not goods_ids:
                """
                {"xxxordersnxx": {"code": 404, "detail": "选中的购物车为空"}}}
                """
                local_execute_dict[order_sn]["code"] = (
                    grpc.StatusCode.NOT_FOUND
                )
                local_execute_dict[order_sn]["detail"] = "选中的购物车为空"
                return TransactionStatus.ROLLBACK

            # 获取商品价格
            register = consul.ConsulRegister(settings.CONSUL_HOST,
                                             settings.CONSUL_PORT)
            goods_srv_host, goods_srv_port = register.get_service_host_port(
                settings.GOODS_SRV_NAME)
            if not goods_srv_host:
                """
                {"xxxordersnxx": {"code": 404, "detail": "选中的购物车为空"}}}
                """
                local_execute_dict[order_sn]["code"] = (
                    grpc.StatusCode.NOT_FOUND
                )
                local_execute_dict[order_sn]["detail"] = "商品服务不存在"
                return TransactionStatus.ROLLBACK

            with grpc.insecure_channel(f"{goods_srv_host}:{goods_srv_port}",
                                       retry_interceptor) as channel:
                goods_stub = goods_pb2_grpc.GoodsStub(channel)
                try:
                    goods_info_rsp = goods_stub.BatchGetGoods(
                        goods_pb2.BatchGoodsIdInfo(id=goods_ids))
                except grpc.RpcError:
                    local_execute_dict[order_sn]["code"] = (
                        grpc.StatusCode.INTERNAL
                    )
                    local_execute_dict[order_sn]["detail"] = "商品服务不可用"
                    return TransactionStatus.ROLLBACK

                for goods_info in goods_info_rsp.data:
                    order_mount += (
                        goods_info.shopPrice * goods_nums[goods_info.id]
                    )
                    order_goods_list.append(OrderGoods(
                        goods=goods_info.id,
                        goods_name=goods_info.name,
                        goods_image=goods_info.goodsFrontImage,
                        goods_price=goods_info.shopPrice,
                        nums=goods_nums[goods_info.id]
                    ))
                    goods_sell_info.append(inventory_pb2.GoodsInvInfo(
                        goodsId=goods_info.id,
                        num=goods_nums[goods_info.id]
                    ))

            # 扣减库存
            inv_srv_host, inv_srv_port = register.get_service_host_port(
                settings.INVENTORY_SRV_NAME)
            if not inv_srv_host:
                """
                {"xxxordersnxx": {"code": 404, "detail": "选中的购物车为空"}}}
                """
                local_execute_dict[order_sn]["code"] = grpc.StatusCode.INTERNAL
                local_execute_dict[order_sn]["detail"] = "库存服务不存在"
                return TransactionStatus.ROLLBACK

            with grpc.insecure_channel(f"{inv_srv_host}:{inv_srv_port}",
                                       retry_interceptor) as channel:
                inv_stub = inventory_pb2_grpc.InventoryStub(channel)

                try:
                    _ = inv_stub.Sell(inventory_pb2.SellInfo(
                        orderSn=order_sn, goodsInfo=goods_sell_info))
                except grpc.RpcError as e:
                    local_execute_dict[order_sn]["code"] = (
                        grpc.StatusCode.INTERNAL
                    )
                    local_execute_dict[order_sn]["detail"] = (
                        f"扣减库存失败: {e.details()}"
                    )
                    err_code = e.code()
                    if err_code in (grpc.StatusCode.UNKNOWN,
                                    grpc.StatusCode.DEADLINE_EXCEEDED):
                        # 库存不足，库存服务没有扣减库存，不需要发送归还库存消息
                        return TransactionStatus.COMMIT
                    else:
                        return TransactionStatus.ROLLBACK

            # 创建订单
            try:
                order = OrderInfo(
                    user=msg_body["userId"],
                    order_sn=order_sn,
                    order_mount=order_mount,
                    address=msg_body["address"],
                    signer_name=msg_body["name"],
                    signer_mobile=msg_body["mobile"],
                    leave_message=msg_body["message"],
                )
                order.save()

                for order_good in order_goods_list:
                    order_good.order = order.id
                OrderGoods.bulk_create(order_goods_list)

                # 删除购物车商品
                ShoppingCart.delete().where(
                    ShoppingCart.user == msg_body["userId"],
                    checked=True).execute()
                local_execute_dict[order_sn]["code"] = grpc.StatusCode.OK
                local_execute_dict[order_sn]["detail"] = "创建订单成功"
                local_execute_dict[order_sn] = {
                    "code": grpc.StatusCode.OK,
                    "detail": "创建订单成功",
                    "order": {
                        "id": order.id,
                        "orderSn": order_sn,
                        "total": order.order_mount,
                    }
                }

                # 发送延时消息
                msg = Message("order_timeout")
                msg.set_delay_time_level(5)
                msg.set_keys("pygo")
                msg.set_tags("cancel")
                msg.set_body(json.dumps({"orderSn": order_sn}))
                sync_producer = Producer("cancel")
                sync_producer.set_name_server_address(
                    f"{settings.ROCKETMQ_HOST}:{settings.ROCKETMQ_PORT}")
                sync_producer.start()

                ret = sync_producer.send_sync(msg)
                if ret.status != SendStatus.OK:
                    raise Exception("发送延时消息失败")

                sync_producer.shutdown()

            except Exception as e:
                txn.rollback()
                local_execute_dict[order_sn]["code"] = grpc.StatusCode.INTERNAL
                local_execute_dict[order_sn]["detail"] = f"创建订单失败: {e}"
                return TransactionStatus.COMMIT

        return TransactionStatus.ROLLBACK

    @logger.catch
    def CreateOrder(self, request: order_pb2.OrderRequest, context):
        """
        创建订单
        1. 获取价格 -- 商品服务
        2. 库存扣减 -- 库存服务
        3. 生成订单 -- 订单服务
        4. 从购物车获取并删除商品 -- 订单服务
        """
        producer = TransactionMQProducer("pygo", self.check_callback)
        producer.set_name_server_address(
            f"{settings.ROCKETMQ_HOST}:{settings.ROCKETMQ_PORT}")
        producer.start()
        msg = Message("order_reback")
        msg.set_keys("pygo")
        msg.set_tags("order")

        order_sn = generate_order_sn(request.userId)
        msg_body = {
            "orderSn": order_sn,
            "userId": request.userId,
            "address": request.address,
            "name": request.name,
            "mobile": request.mobile,
            "message": request.message,
        }
        msg.set_body(json.dumps(msg_body))

        ret = producer.send_message_in_transaction(msg, self.local_execute,
                                                   user_args=None)
        logger.info(f"发送状态: {ret.status}，消息ID: {ret.msg_id}")
        if ret.status != SendStatus.OK:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("发送消息失败")
            return order_pb2.OrderInfoResponse()

        while True:
            if order_sn in local_execute_dict:
                context.set_code(local_execute_dict[order_sn]["code"])
                context.set_details(local_execute_dict[order_sn]["detail"])
                producer.shutdown()
                if local_execute_dict[order_sn]["code"] == grpc.StatusCode.OK:
                    return order_pb2.OrderInfoResponse(
                        **local_execute_dict[order_sn]["order"])
                else:
                    return order_pb2.OrderInfoResponse()
            time.sleep(0.1)
