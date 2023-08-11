import json

import consul
import grpc

from goods_srv.proto import category_pb2, category_pb2_grpc
from goods_srv.settings import settings

from google.protobuf import empty_pb2


class CategoryTest:
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
        self.stub = category_pb2_grpc.CategoryStub(channel)

    def category_list(self):
        rsp: category_pb2.CategoryListResponse = (
            self.stub.GetAllCategorysList(empty_pb2.Empty())
        )
        data = json.loads(rsp.jsonData)
        print(data)

    def sub_category_list(self, id):
        rsp: category_pb2.SubCategoryListResponse = self.stub.GetSubCategory(
            category_pb2.CategoryListRequest(id=id)
        )
        print(rsp.subCategorys, rsp.info)


if __name__ == "__main__":
    category = CategoryTest()
    # category.category_list()
    category.sub_category_list(136690)
