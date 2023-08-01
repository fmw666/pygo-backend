import os
import sys
# append ../ to sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "../"))

import time
import json

import consul
import grpc

from goods_srv.proto import brand_pb2, brand_pb2_grpc
from goods_srv.settings import settings

from google.protobuf import empty_pb2


class BrandTest:
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
        self.stub = brand_pb2_grpc.BrandStub(channel)

    def brand_list(self):
        rsp: brand_pb2.BrandListResponse = self.stub.BrandList(empty_pb2.Empty())
        print(rsp)
    
    # def create_banner(self, image, index, url):
    #     rsp: banner_pb2.BannerResponse = self.stub.CreateBanner(
    #         banner_pb2.BannerRequest(
    #             image=image,
    #             index=index,
    #             url=url,
    #         )
    #     )
    #     print(rsp)
    
    # def delete_banner(self, id):
    #     self.stub.DeleteBanner(banner_pb2.BannerRequest(id=id))


if __name__ == "__main__":
    brand = BrandTest()
    brand.brand_list()
    