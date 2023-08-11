
import consul
import grpc

from goods_srv.proto import goods_pb2, goods_pb2_grpc
from goods_srv.settings import settings


class GoodsTest:
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
        self.stub = goods_pb2_grpc.GoodsStub(channel)

    def goods_list(self):
        rsp: goods_pb2.GoodsListResponse = self.stub.GoodsList(
            goods_pb2.GoodsFilterRequest(priceMin=50)
        )
        print(rsp.total)
        for good in rsp.data:
            print(good.name, good.shopPrice)

    def batch_get(self):
        ids = [421, 422]
        rsp: goods_pb2.GoodsListResponse = self.stub.BatchGetGoods(
            goods_pb2.BatchGoodsIdInfo(id=ids)
        )
        print(rsp.total)
        for good in rsp.data:
            print(good.name, good.shopPrice)

    def get_detail(self, id):
        rsp: goods_pb2.GoodsInfoResponse = self.stub.GetGoodsDetail(
            goods_pb2.GoodInfoRequest(id=id)
        )
        print(rsp.name, rsp.shopPrice, rsp.clickNum)


if __name__ == "__main__":
    goods = GoodsTest()
    # goods.goods_list()
    # goods.batch_get()
    goods.get_detail(421)
