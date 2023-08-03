"""
0. 读取 config.ini 文件，读取配置信息
1. 将配置信息写入到 jenkinscfg 目录下的 xml 文件中
2. 将配置信息...
"""
import os
import sys
# append ../ to sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "../"))

import xml.etree.ElementTree as ET

from scripts.utils.common import config


parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(getattr(config.DockerServer, "nacos_port"))


# 修改 ../jenkinscfg/*.xml 配置文件
credential_names = ["credential_git", "credential_ssh"]
for c_name in credential_names:
    xml_path = os.path.join(parent_dir, "jenkinscfg", f"{c_name}.xml")
    tree = ET.parse(xml_path)
    root = tree.getroot()
    for tag in ["id", "description", "username", "password"]:
        sub = root.find(tag)
        sub.text = getattr(config.Jenkins, f"{c_name}_{tag}")
    tree.write(xml_path, encoding="utf-8", xml_declaration=False)

xml_path = os.path.join(parent_dir, "jenkinscfg", "job_pipeline.xml")
tree = ET.parse(xml_path)
print(tree.findall("url"))

root = tree.getroot()
sub_url = root.find("url")
sub_url.text = config.GitServer.srv_repo
sub_credentialsId = root.find("credentialsId")
sub_credentialsId.text = config.Jenkins.credential_git_id
tree.write(xml_path, encoding="utf-8", xml_declaration=False)
