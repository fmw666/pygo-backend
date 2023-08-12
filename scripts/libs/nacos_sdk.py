import json

import requests


HTTP_STATUS_OK = 200


class NacosClient:
    """提供 Nacos 的接口封装"""

    # 前缀 http://
    PREFIX = "http://"
    SERVER_STATE_URL = "/nacos/v1/console/server/state"
    ALL_NAMESPACES_URL = "/nacos/v1/console/namespaces"
    ALL_CONFIGS_URL = "/nacos/v1/cs/configs"

    def __init__(self, host: str, port: int, user: str, password: str) -> None:
        """
        初始化方法
        :param host: Nacos 服务的 IP
        :param port: Nacos 服务的端口
        :param user: Nacos 服务的用户名
        :param password: Nacos 服务的密码
        :return: None
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def get_version(self) -> None | str:
        """
        http://127.0.0.1:8848/nacos/v1/console/server/state
        {..., "version":"2.2.3"}
        """
        rsp = requests.get(f"{self.PREFIX}{self.host}:{self.port}"
                           f"{self.SERVER_STATE_URL}")
        if rsp.status_code != HTTP_STATUS_OK:
            return None

        json_data = rsp.json()
        return json_data.get("version")

    def get_all_namespaces(self) -> None | list[dict]:
        """
        :returns: [
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
        """
        rsp = requests.get(f"{self.PREFIX}{self.host}:{self.port}"
                           f"{self.ALL_NAMESPACES_URL}")
        if rsp.status_code != HTTP_STATUS_OK:
            raise requests.exceptions.HTTPError(f"HTTP 错误，状态码: "
                                                f"{rsp.status_code}")

        json_data = rsp.json()
        if json_data["code"] != HTTP_STATUS_OK:
            raise requests.exceptions.HTTPError(f"HTTP 错误，状态码: "
                                                f"{rsp.status_code}")

        return json_data.get("data")

    def check_namespace_exist_by_name(self, namespace_name: str) -> bool:
        """
        通过 namespace 名称检查是否存在
        :param namespace_name: namespace 名称
        :return: bool
        """
        all_namespaces = self.get_all_namespaces()
        for namespace in all_namespaces:
            if namespace["namespaceShowName"] == namespace_name:
                return True
        return False

    def check_namespace_exist_by_id(self,
                                    namespace_id: str,
                                    namespace_name: str = "") -> bool:
        """
        http://127.0.0.1:8848/nacos/v1/console/namespaces\
            ?checkNamespaceIdExist=true&customNamespaceId=&namespaceId={test}
        :param namespace_id: namespace id
        :param namespace_name: namespace name
        :return: bool
        """
        params = {
            "checkNamespaceIdExist": "true",
            "namespaceId": namespace_name,
            "customNamespaceId": namespace_id
        }
        rsp = requests.get(f"{self.PREFIX}{self.host}:{self.port}"
                           f"{self.ALL_NAMESPACES_URL}", params=params)
        if rsp.status_code != HTTP_STATUS_OK:
            raise requests.exceptions.HTTPError(f"HTTP 错误，状态码: "
                                                f"{rsp.status_code}")
        return rsp.json()

    def get_namespace_by_id(self, namespace_id: str) -> None | dict:
        """
        通过 namespace id 获取 namespace 信息
        :param namespace_id: namespace id
        :return: {
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

    def get_namespaces_by_name(self,
                               namespace_name: str) -> None | list[dict]:
        """
        通过 namespace name 获取 namespace 信息
        :param namespace_name: namespace name
        :return: [
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

    def delete_namespace_by_id(self, namespace_id: str) -> bool:
        """
        通过 namespace id 删除 namespace
        http://127.0.0.1:8848/nacos/v1/console/namespaces?namespaceId={test-namespace}

        :param namespace_id: namespace id
        :return: bool
        """
        rsp = requests.delete(f"{self.PREFIX}{self.host}:{self.port}"
                              f"{self.ALL_NAMESPACES_URL}",
                              params={"namespaceId": namespace_id})

        if rsp.status_code != HTTP_STATUS_OK:
            raise requests.exceptions.HTTPError(f"HTTP 错误，状态码: "
                                                f"{rsp.status_code}")
        return rsp.json()

    def create_namespace(self,
                         namespace_id: str = "",
                         *,
                         namespace_name: str,
                         namespace_desc: str) -> bool:
        """
        创建 namespace
        :param namespace_id: namespace id
        :param namespace_name: namespace name
        :param namespace_desc: namespace desc
        :return: bool
        """
        data = {
            "customNamespaceId": namespace_id,
            "namespaceName": namespace_name,
            "namespaceDesc": namespace_desc,
            "namespaceId": namespace_name,
        }

        rsp = requests.post(f"{self.PREFIX}{self.host}:{self.port}"
                            f"{self.ALL_NAMESPACES_URL}", data=data)

        if rsp.status_code != HTTP_STATUS_OK:
            raise requests.exceptions.HTTPError(f"HTTP 错误，状态码: "
                                                f"{rsp.status_code}")
        return rsp.json()

    def get_configs_namespace_id(self,
                                 namespace_id: str,
                                 dataId: str = "",
                                 group: str = "",
                                 pageNo: int = 1,
                                 pageSize: int = 999) -> None | list[dict]:
        """
        http://127.0.0.1:8848/nacos/v1/cs/configs?\
            dataId=&group=&appName=&config_tags=&pageNo=1&pageSize=999&\
            tenant=068d14d8-6b29-498f-b824-40e92e03a3bd&search=blur
        :param namespace_id: namespace id
        :param dataId: dataId
        :param group: group
        :param pageNo: pageNo
        :param pageSize: pageSize
        :return: [
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
        rsp = requests.get(f"{self.PREFIX}{self.host}:{self.port}"
                           f"{self.ALL_CONFIGS_URL}", params=params)

        if rsp.status_code != HTTP_STATUS_OK:
            raise requests.exceptions.HTTPError(f"HTTP 错误，状态码: "
                                                f"{rsp.status_code}")

        json_data = rsp.json()
        for item in json_data["pageItems"]:
            item["content"] = json.loads(item["content"])
        return json_data["pageItems"]

    def import_configs_by_namespace_id(self,
                                       namespace_id: str,
                                       file_path) -> dict:
        """
        http://127.0.0.1:8848/nacos/v1/cs/configs?\
            import=true&namespace=37fc7fc3-ba6f-4194-8a60-baa1e00fefe4&\
            accessToken=&username=&tenant=37fc7fc3-ba6f-4194-8a60-baa1e00fefe4
        :param namespace_id: namespace id
        :param file_path: file path
        :return: dict
        """
        params = {
            "import": "true",
            "namespace": namespace_id,
            "tenant": namespace_id,
            "accessToken": "",
            "username": "",
        }
        # policy: OVERWRITE, ABORT, SKIP
        data = {
            "policy": "OVERWRITE",
        }
        files = {
            "file": open(file_path, "rb")
        }
        rsp = requests.post(f"{self.PREFIX}{self.host}:{self.port}"
                            f"{self.ALL_CONFIGS_URL}",
                            params=params, data=data, files=files)

        if rsp.status_code != HTTP_STATUS_OK:
            raise requests.exceptions.HTTPError(f"HTTP 错误，状态码: "
                                                f"{rsp.status_code}")
        return rsp.json()
