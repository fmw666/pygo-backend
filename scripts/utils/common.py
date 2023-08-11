import os
# import sys
# append ../ to sys.path
# sys.path.append(os.path.join(os.path.dirname(os.path.dirname(\
# os.path.abspath(__file__))), "../"))

import pymysql
import jenkins

from libs.config_reader import ConfigReader
from libs.nacos_sdk import NacosClient


parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(parent_dir, "config.local.ini")
if not os.path.exists(config_path):
    raise FileNotFoundError(f"配置文件 {config_path} 不存在.")


config = ConfigReader(config_path)


class ServiceNotAvailable(Exception):
    """服务不可用异常"""
    pass


def get_nacos_client() -> NacosClient:
    """
    获取 nacos client.
    :param: None
    :return: NacosClient
    """
    nacos = NacosClient(
        host=config.DockerServer.host,
        port=config.Nacos.port,
        user=config.Nacos.user,
        password=config.Nacos.password,
    )
    if nacos.get_version() is None:
        raise ServiceNotAvailable("nacos 服务不可用.")
    return nacos


def get_jenkins_client() -> jenkins.Jenkins:
    """
    获取 jenkins client.
    :param: None
    :return: jenkins.Jenkins
    """
    jk = jenkins.Jenkins(
        url=f"http://{config.DockerServer.host}:{config.Jenkins.port}",
        username=config.Jenkins.username,
        password=config.Jenkins.password,
    )
    try:
        jk.get_whoami()
    except Exception as e:
        raise ServiceNotAvailable(f"jenkins 服务不可用: {e}")
    return jk


def get_mysql_cursor() -> pymysql.cursors.Cursor:
    """
    获取 mysql cursor.
    :param: None
    :return: pymysql.cursors.Cursor
    """
    try:
        conn = pymysql.connect(
            host=config.DockerServer.host,
            port=int(config.Mysql.port),
            user=config.Mysql.user,
            password=config.Mysql.password
        )
    except Exception as e:
        raise ServiceNotAvailable(f"mysql 服务不可用: {e}")
    return conn.cursor()
