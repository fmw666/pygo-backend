import json
import nacos
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin
from loguru import logger


class ReconnectMysqlDatabase(ReconnectMixin, PooledMySQLDatabase):
    pass


NACOS = {
    "Host": "192.168.1.2",
    "Port": 8848,
    "NameSpace": "068d14d8-6b29-498f-b824-40e92e03a3bd",
    "User": "nacos",
    "Password": "nacos",
    "DataId": "user-srv.json",
    "Group": "dev",
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

# Consul
CONSUL_HOST = data["consul"]["host"]
CONSUL_PORT = data["consul"]["port"]

# Service
SERVICE_NAME = data["name"]
SERVICE_TAGS = data["tags"]
