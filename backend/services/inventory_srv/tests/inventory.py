
import consul
import grpc

from inventory_srv.proto import inventory_pb2, inventory_pb2_grpc
from inventory_srv.settings import settings


class InventoryTest:
    def __init__(self) -> None:
        # try to connect to the server
        c = consul.Consul(host="127.0.0.1", port=8500)
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
        self.stub = inventory_pb2_grpc.InventoryStub(channel)

    def set_inv(self):
        self.stub.SetInv(
            inventory_pb2.GoodsInvInfo(goodsId=10, num=90)
        )

    def get_inv(self):
        rsp: inventory_pb2.GoodsInvInfo = self.stub.InvDetail(
            inventory_pb2.GoodsInvInfo(goodsId=10)
        )
        print(rsp.num)


if __name__ == "__main__":
    inv = InventoryTest()
    # inv.set_inv()
    inv.get_inv()
