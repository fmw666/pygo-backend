import json

from common.lock.py_redis_lock import Lock
from inventory_srv.model.models import Inventory, InventoryHistory
from inventory_srv.proto import inventory_pb2, inventory_pb2_grpc
from inventory_srv.settings import settings

import grpc
from google.protobuf import empty_pb2
from loguru import logger
from peewee import DoesNotExist
from rocketmq.client import ConsumeStatus


def reback_inventory(msg):
    """
    通过 msg body 中的 order_sn 确认归还库存
    """
    msg_body = json.loads(msg.body.decode("utf-8"))
    order_sn = msg_body["orderSn"]

    with settings.DB.atomic() as txn:
        try:
            inv_history = InventoryHistory.get(
                InventoryHistory.order_sn==order_sn, InventoryHistory.status==1
            )
            inv_details = json.loads(inv_history.order_inv_detail)
            for item in inv_details:
                goods_id = item["goods_id"]
                num = item["num"]
                Inventory.update(stocks=Inventory.stocks+num).where(Inventory.goods==goods_id).execute()
            inv_history.status = 2
            inv_history.save()
            return ConsumeStatus.CONSUME_SUCCESS
        except DoesNotExist:
            return ConsumeStatus.CONSUME_SUCCESS
        except Exception:
            txn.rollback()
            return ConsumeStatus.RECONSUME_LATER


class InventoryServicer(inventory_pb2_grpc.InventoryServicer):

    @logger.catch
    def SetInv(self, request: inventory_pb2.GoodsInvInfo, context):
        """
        设置商品库存
        """
        force_insert = False
        inv = Inventory.select().where(Inventory.goods == request.goodsId).first()
        if not inv:
            inv = Inventory()
            inv.goods = request.goodsId
            force_insert = True
        inv.stocks = request.num
        inv.save(force_insert=force_insert)

        return empty_pb2.Empty()
    
    @logger.catch
    def InvDetail(self, request: inventory_pb2.GoodsInvInfo, context):
        """
        获取某个商品库存详情
        """
        inv = Inventory.select().where(Inventory.goods == request.goodsId).first()
        if not inv:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("inventory not found")
            return inventory_pb2.GoodsInvInfo()
        return inventory_pb2.GoodsInvInfo(goodsId=inv.goods, num=inv.stocks)
    
    @logger.catch
    def Sell(self, request: inventory_pb2.SellInfo, context):
        """
        扣减库存

        解决超卖问题，使用 peewee 事务
        """
        inv_history = InventoryHistory(order_sn=request.orderSn)
        inv_details = []
        with settings.DB.atomic() as txn:
            for item in request.goodsInfo:
                lock = Lock(settings.REDIS_CLIENT, f"lock:goods:{item.goodsId}", auto_renewal=True, expire=10)
                lock.acquire()
                goods_inv = Inventory.select().where(Inventory.goods == item.goodsId).first()
                # 库存不存在或者库存不足
                if not goods_inv:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("inventory not found")
                    txn.rollback()
                    return empty_pb2.Empty()
                if goods_inv.stocks < item.num:
                    context.set_code(grpc.StatusCode.RESOURCE_EXHAUSTED)
                    context.set_details("insufficient inventory")
                    txn.rollback()
                    return empty_pb2.Empty()
                # 扣减库存
                inv_details.append({"goods_id": item.goodsId, "num": item.num})
                goods_inv.stocks -= item.num
                goods_inv.save()
                lock.release()
        
            inv_history.order_inv_detail = json.dumps(inv_details)
            inv_history.save()
            return empty_pb2.Empty()
    
    @logger.catch
    def Reback(self, request: inventory_pb2.GoodsInvInfo, context):
        """
        归还库存
        1. 订单超时
        2. 订单创建失败
        3. 订单取消
        """
        with settings.DB.atomic() as txn:
            for item in request.goodsInfo:
                lock = Lock(settings.REDIS_CLIENT, f"lock:goods:{item.goodsId}", auto_renewal=True, expire=10)
                lock.acquire()
                goods_inv = Inventory.select().where(Inventory.goods == item.goodsId).first()
                # 库存不存在或者库存不足
                if not goods_inv:
                    context.set_code(grpc.StatusCode.NOT_FOUND)
                    context.set_details("inventory not found")
                    txn.rollback()
                    return empty_pb2.Empty()
                # 归还库存    
                goods_inv.stocks += item.num
                goods_inv.save()
                lock.release()
        
        return empty_pb2.Empty()
    