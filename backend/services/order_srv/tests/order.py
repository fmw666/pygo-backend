import os
import sys
# append ../ to sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "../"))

import time

import consul
import grpc

from order_srv.proto import order_pb2, order_pb2_grpc
from order_srv.settings import settings


class OrderTest:
    def __init__(self) -> None:
        # try to connect to the server
        c = consul.Consul(host=settings.CONSUL_HOST, port=settings.CONSUL_PORT)
        services = c.agent.services()
        
        ip = ""
        port = ""
        for _, v in services.items():
            if v["Service"] == settings.SERVICE_NAME:
                ip = v["Address"]
                port = v["Port"]
                break
        
        if ip == "" or port == "":
            raise Exception("no service available")
        
        channel = grpc.insecure_channel(f"{ip}:{port}")
        self.stub = order_pb2_grpc.OrderStub(channel)
    
    def cart_item_list(self):
        rsp = self.stub.CartItemList(
            order_pb2.UserInfoRequest(id=1)
        )
        print(rsp)

    def create_cart_item(self):
        rsp = self.stub.CreateCartItem(
            order_pb2.CartItemRequest(goodsId=422, userId=1, nums=3)
        )
        print(rsp)
    
    def create_order(self):
        rsp = self.stub.CreateOrder(
            order_pb2.OrderRequest(
                userId=4,
                address="四川省自贡市",
                mobile="12345678901",
                name="范茂伟",
                message="请尽快发货",
            )
        )
        print(rsp)
    
    def order_list(self):
        rsp = self.stub.OrderList(order_pb2.OrderFilterRequest(userId=1))
        print(rsp)
    
    def order_detail(self):
        rsp = self.stub.OrderDetail(order_pb2.OrderRequest(userId=4, id=1))
        print(rsp)
    
    def update_order_status(self):
        self.stub.UpdateOrderStatus(
            order_pb2.OrderStatusRequest(orderSn="20230722143834211", status="TRADE_SUCCESS")
        )
    

if __name__ == "__main__":
    ot = OrderTest()
    # ot.create_cart_item()
    # ot.create_order()
    # ot.order_list()
    # ot.cart_item_list()
    # ot.order_detail()
    ot.update_order_status()
