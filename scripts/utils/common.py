import os
import sys
# append ../ to sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "../"))

import jenkins

from scripts.libs.config_reader import ConfigReader
from scripts.libs.nacos_sdk import NacosClient


parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(parent_dir, "config.ini")
if not os.path.exists(config_path):
    print(f"配置文件 {config_path} 不存在.")
    sys.exit(1)


config = ConfigReader(os.path.join(parent_dir, "config.ini"))


def get_nacos_client() -> NacosClient:
    nacos = NacosClient(
        host=config.DockerServer.host,
        port=config.DockerServer.nacos_port,
        user=config.DockerServer.nacos_user,
        password=config.DockerServer.nacos_password,
    )
    if nacos.get_version() is None:
        print("nacos 服务不可用.")
        sys.exit(1)
    return nacos

def get_jenkins_client() -> jenkins.Jenkins:
    jk = jenkins.Jenkins(
        url=f"http://{config.DockerServer.host}:{config.Jenkins.port}",
        username=config.Jenkins.username,
        password=config.Jenkins.password,
    )
    try:
        jk.get_whoami()
    except Exception as e:
        print(f"jenkins 服务不可用: {e}")
        sys.exit(1)
    return jk
