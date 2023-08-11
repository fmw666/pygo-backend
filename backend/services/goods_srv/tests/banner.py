
import consul
import grpc

from goods_srv.proto import banner_pb2, banner_pb2_grpc
from goods_srv.settings import settings

from google.protobuf import empty_pb2


class BannerTest:
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
        self.stub = banner_pb2_grpc.BannerStub(channel)

    def banner_list(self):
        rsp: banner_pb2.BannerListResponse = (
            self.stub.BannerList(empty_pb2.Empty())
        )
        print(rsp)

    def create_banner(self, image, index, url):
        rsp: banner_pb2.BannerResponse = self.stub.CreateBanner(
            banner_pb2.BannerRequest(
                image=image,
                index=index,
                url=url,
            )
        )
        print(rsp)

    def delete_banner(self, id):
        self.stub.DeleteBanner(banner_pb2.BannerRequest(id=id))


if __name__ == "__main__":
    banner = BannerTest()
    # banner.banner_list()
    # banner.create_banner("http://www.baidu.com", 1, "http://www.baidu.com")
    # banner.delete_banner(5)
