import json
from typing import Optional

import requests


class NacosClient:
    
    def __init__(self, host: str, port: int, user: str, password: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def get_all_namespaces(self) -> Optional[list[dict]]:
        """
        returns: {
            "code": 200,
            "message": null,
            "data": [
                {
                    "namespace": "",
                    "namespaceShowName": "public",
                    "namespaceDesc": null,
                    "quota": 200,
                    "configCount": 0,
                    "type": 0
                },
                {
                    "namespace": "068d14d8-6b29-498f-b824-40e92e03a3bd",
                    "namespaceShowName": "users",
                    "namespaceDesc": "用户服务",
                    "quota": 200,
                    "configCount": 4,
                    "type": 2
                },
                ...
            ]
        }
        """
        rsp = requests.get(f"http://{self.host}:{self.port}/nacos/v1/console/namespaces")
        
        if rsp.status_code != 200:
            raise Exception(f"get all namespaces failed: {rsp.text}")
        
        json_data = rsp.json()
        if json_data["code"] != 200:
            raise Exception(f"get all namespaces failed: {json_data['message']}")
        
        return json_data["data"]


    def check_namespace_exist_by_name(self, namespace_name: str) -> bool:
        all_namespaces = self.get_all_namespaces()
        for namespace in all_namespaces:
            if namespace["namespaceShowName"] == namespace_name:
                return True
        return False


    def check_namespace_exist_by_id(self, namespace_id: str, namespace_name: str = "") -> bool:
        """
        http://127.0.0.1:8848/nacos/v1/console/namespaces?checkNamespaceIdExist=true&customNamespaceId=&namespaceId={test}
        """
        params = {
            "checkNamespaceIdExist": "true",
            "namespaceId": namespace_name,
            "customNamespaceId": namespace_id
        }
        rsp = requests.get(f"http://{self.host}:{self.port}/nacos/v1/console/namespaces", params=params)
        
        if rsp.status_code != 200:
            raise Exception(f"check namespace exist failed: {rsp.text}")
        return rsp.json()


    def get_namespace_by_id(self, namespace_id: str) -> Optional[dict]:
        """
        returns: {
            "namespace": "068d14d8-6b29-498f-b824-40e92e03a3bd",
            "namespaceShowName": "users",
            "namespaceDesc": "用户服务",
            "quota": 200,
            "configCount": 4,
            "type": 2
        }
        """
        all_namespaces = self.get_all_namespaces()
        for namespace in all_namespaces:
            if namespace["namespace"] == namespace_id:
                return namespace
        return None
    

    def get_namespaces_by_name(self, namespace_name: str) -> Optional[list[dict]]:
        """
        returns: [
            {
                "namespace": "068d14d8-6b29-498f-b824-40e92e03a3bd",
                "namespaceShowName": "users",
                "namespaceDesc": "用户服务",
                "quota": 200,
                "configCount": 4,
                "type": 2
            },
            ...
        ]
        """
        all_namespaces = self.get_all_namespaces()
        namespaces = []
        for namespace in all_namespaces:
            if namespace["namespaceShowName"] == namespace_name:
                namespaces.append(namespace)
        return namespaces


    def delete_namespace_by_id(self, namespace_id: str) -> None:
        """
        http://127.0.0.1:8848/nacos/v1/console/namespaces?namespaceId={test-namespace}
        delete namespace by namespace_id
        """
        rsp = requests.delete(f"http://{self.host}:{self.port}/nacos/v1/console/namespaces", params={"namespaceId": namespace_id})
        
        if rsp.status_code != 200:
            raise Exception(f"delete namespace failed: {rsp.text}")
        return rsp.json()


    def create_namespace(self, namespace_id: str = "", *, namespace_name: str, namespace_desc: str):
        """
        """
        data = {
            "customNamespaceId": namespace_id,
            "namespaceName": namespace_name,
            "namespaceDesc": namespace_desc,
            "namespaceId": namespace_name,
        }

        rsp = requests.post(f"http://{self.host}:{self.port}/nacos/v1/console/namespaces", data=data)
        
        if rsp.status_code != 200:
            raise Exception(f"create namespace failed: {rsp.text}")
        return rsp.json()


    def get_configs_namespace_id(
            self,
            namespace_id: str,
            dataId: str = "",
            group: str = "",
            pageNo: int = 1,
            pageSize: int = 999,
        ) -> Optional[list[dict]]:
        """
        http://127.0.0.1:8848/nacos/v1/cs/configs?\
            dataId=&group=&appName=&config_tags=&pageNo=1&pageSize=999&\
            tenant=068d14d8-6b29-498f-b824-40e92e03a3bd&search=blur
        
        returns: [
            {
                "id": "655407060690681856",
                "dataId": "user-srv.json",
                "group": "dev",
                "content": <json data>,
                "md5": null,
                "encryptedDataKey": "",
                "tenant": "068d14d8-6b29-498f-b824-40e92e03a3bd",
                "appName": "",
                "type": null
            },
            ...
        ]
        """
        params = {
            "dataId": dataId,
            "group": group,
            "appName": "",
            "config_tags": "",
            "pageNo": pageNo,
            "pageSize": pageSize,
            "tenant": namespace_id,
            "search": "blur"
        }
        rsp = requests.get(f"http://{self.host}:{self.port}/nacos/v1/cs/configs", params=params)

        if rsp.status_code != 200:
            raise Exception(f"get configs failed: {rsp.text}")
        
        json_data = rsp.json()
        for item in json_data["pageItems"]:
            item["content"] = json.loads(item["content"])
        return json_data["pageItems"]
    

    def import_configs_by_namespace_id(self, namespace_id: str, file_path) -> dict:
        """
        http://127.0.0.1:8848/nacos/v1/cs/configs?\
            import=true&namespace=37fc7fc3-ba6f-4194-8a60-baa1e00fefe4&\
            accessToken=&username=&tenant=37fc7fc3-ba6f-4194-8a60-baa1e00fefe4
        """
        params = {
            "import": "true",
            "namespace": namespace_id,
            "tenant": namespace_id,
            "accessToken": "",
            "username": "",
        }
        files = {
            "file": open(file_path, "rb")
        }
        rsp = requests.post(f"http://{self.host}:{self.port}/nacos/v1/cs/configs", params=params, files=files)

        if rsp.status_code != 200:
            raise Exception(f"import configs failed: {rsp.text}")
        return rsp.json()
