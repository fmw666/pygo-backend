import json

import redis
import nacos
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin
from loguru import logger


class ReconnectMysqlDatabase(ReconnectMixin, PooledMySQLDatabase):
    pass


NACOS = {
    "Host": "192.168.1.2",
    "Port": 8848,
    "NameSpace": "d3ea228f-7e26-441f-9a92-a1742354e796",
    "User": "nacos",
    "Password": "nacos",
    "DataId": "inventory-srv.json",
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

# RocketMQ
ROCKETMQ_HOST = data["rocketmq"]["host"]
ROCKETMQ_PORT = data["rocketmq"]["port"]

# Service
SERVICE_NAME = data["name"]
SERVICE_TAGS = data["tags"]

# Redis
REDIS_HOST = data["redis"]["host"]
REDIS_PORT = data["redis"]["port"]
REDIS_DB = data["redis"]["db"]

pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
REDIS_CLIENT = redis.StrictRedis(connection_pool=pool)
