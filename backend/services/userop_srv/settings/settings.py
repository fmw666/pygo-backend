import os
import json
import nacos
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin
from loguru import logger


class ReconnectMysqlDatabase(ReconnectMixin, PooledMySQLDatabase):
    pass


config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")
config_json_data = json.loads(open(config_path, "r", encoding="utf-8").read())

NACOS = {
    "Host": config_json_data["nacos"]["host"],
    "Port": config_json_data["nacos"]["port"],
    "NameSpace": config_json_data["nacos"]["namespace"],
    "User": config_json_data["nacos"]["user"],
    "Password": config_json_data["nacos"]["password"],
    "DataId": config_json_data["nacos"]["data_id"],
    "Group": config_json_data["nacos"]["group"],
}

client = nacos.NacosClient(
    f"{NACOS['Host']}:{NACOS['Port']}",
    namespace=NACOS["NameSpace"],
    username=NACOS["User"],
    password=NACOS["Password"],
)
data = client.get_config(NACOS["DataId"], NACOS["Group"])
data = json.loads(data)
logger.info(f"get config from nacos: {data}")

def update_cfg(args):
    global data
    data = json.loads(args)
    logger.info(f"update config from nacos: {data}")

DB = ReconnectMysqlDatabase(
    data["mysql"]["db"],
    host=data["mysql"]["host"],
    port=data["mysql"]["port"],
    user=data["mysql"]["user"],
    password=data["mysql"]["password"],
)

# Host
HOST = data["host"]

# Consul
CONSUL_HOST = data["consul"]["host"]
CONSUL_PORT = data["consul"]["port"]

# Service
SERVICE_NAME = data["name"]
SERVICE_TAGS = data["tags"]
