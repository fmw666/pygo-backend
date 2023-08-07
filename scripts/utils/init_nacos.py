"""
1. 删除所有 id 相同的命名空间，创建新的命名空间.
2. 向各命名空间中导入 nacosfiles 下的配置文件.
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from scripts.utils.common import get_nacos_client, config


parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
client = get_nacos_client()


def create_namespace_and_import_config() -> None:
    srvs_list = ["goods", "inventory", "order", "user", "userop"]
    for srv in srvs_list:
        if client.check_namespace_exist_by_id(getattr(config.Nacos, f"{srv}_namespace_id")):
            client.delete_namespace_by_id(getattr(config.Nacos, f"{srv}_namespace_id"))
        client.create_namespace(
            namespace_id=getattr(config.Nacos, f"{srv}_namespace_id"),
            namespace_name=getattr(config.Nacos, f"{srv}_namespace_name"),
            namespace_desc=getattr(config.Nacos, f"{srv}_namespace_desc"),
        )
        nacos_config_file_path = os.path.join(parent_dir, "nacosfiles", f"{srv}_config.zip")
        print(client.import_configs_by_namespace_id(
            namespace_id=getattr(config.Nacos, f"{srv}_namespace_id"),
            file_path=nacos_config_file_path
        ))


def execute() -> None:
    create_namespace_and_import_config()


if __name__ == "__main__":
    execute()
