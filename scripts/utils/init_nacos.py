"""
1. 删除所有 id 相同的命名空间，创建新的命名空间.
2. 向各命名空间中导入 nacosfiles 下的配置文件.
"""
import os

from libs.nacos_sdk import NacosClient
from utils.common import get_nacos_client, config


parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_namespace_and_import_config(client: NacosClient) -> None:
    """
    1. 删除所有 id 相同的命名空间，创建新的命名空间.
    2. 向各命名空间中导入 nacosfiles 下的配置文件.

    :param client: NacosClient
    :return: None
    """
    srvs_list = ["goods", "inventory", "order", "user", "userop"]
    for srv in srvs_list:
        if client.check_namespace_exist_by_id(
            getattr(config.Nacos, f"{srv}_namespace_id")
        ):
            client.delete_namespace_by_id(
                getattr(config.Nacos, f"{srv}_namespace_id")
            )
        client.create_namespace(
            namespace_id=getattr(config.Nacos, f"{srv}_namespace_id"),
            namespace_name=getattr(config.Nacos, f"{srv}_namespace_name"),
            namespace_desc=getattr(config.Nacos, f"{srv}_namespace_desc"),
        )
        nacos_config_file_path = os.path.join(parent_dir,
                                              "nacosfiles",
                                              f"{srv}_config.zip")
        print(client.import_configs_by_namespace_id(
            namespace_id=getattr(config.Nacos, f"{srv}_namespace_id"),
            file_path=nacos_config_file_path
        ))


def execute() -> None:
    """
    执行创建命名空间和导入配置文件.
    :param: None
    :return: None
    """
    client = get_nacos_client()
    create_namespace_and_import_config(client)


if __name__ == "__main__":
    execute()
