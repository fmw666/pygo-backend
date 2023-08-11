"""
0. 读取 config.ini 文件，读取配置信息
1. 将配置信息写入到 jenkinscfg 目录下的 xml 文件中
2. 将配置信息写入到 nacosfiles 目录下的 zip 文件中
2. 将配置信息写入到 backend 目录下的 services/ config.json
3. 将配置信息写入到 backend 目录下的 apis/ config.yaml
"""
import os
import re
import json
import shutil
import yaml
import zipfile
import xml.etree.ElementTree as ET

from utils.common import config


parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_dir = os.path.dirname(parent_dir)


def rewrite_json_file(json_file_path: str, srv_name: str) -> None:
    """
    重写 json 文件.
    :param json_file_path: 传入的 json 文件路径
    :param srv_name: 要修改的服务名
    :return: None
    """
    json_data = {}
    with open(json_file_path, "r", encoding="utf-8") as f:
        json_data = json.load(f)
    # 修改 json 文件
    json_data["host"] = config.RemoteServer.host
    if "mysql" in json_data:
        json_data["mysql"]["db"] = getattr(config.Mysql, f"{srv_name}_srv_db")
        json_data["mysql"]["host"] = config.DockerServer.host
        json_data["mysql"]["port"] = int(config.Mysql.port)
        json_data["mysql"]["user"] = config.Mysql.user
        json_data["mysql"]["password"] = config.Mysql.password
    for tag in ["redis", "consul", "jaeger", "rocketmq"]:
        if tag in json_data:
            json_data[tag]["host"] = config.DockerServer.host
            json_data[tag]["port"] = int(
                getattr(config.DockerServer, f"{tag}_port")
            )
    if "oss" in json_data:
        json_data["oss"]["key"] = config.AliOss.key
        json_data["oss"]["secrect"] = config.AliOss.secrect
        json_data["oss"]["host"] = config.AliOss.host
        json_data["oss"]["callback_url"] = config.AliOss.callback_url
        json_data["oss"]["upload_dir"] = config.AliOss.upload_dir
    if "alipay" in json_data:
        json_data["alipay"]["app_id"] = config.AliPay.app_id
        json_data["alipay"]["private_key"] = config.AliPay.private_key
        json_data["alipay"]["ali_public_key"] = config.AliPay.ali_public_key
        json_data["alipay"]["notify_url"] = config.AliPay.notify_url
        json_data["alipay"]["return_url"] = config.AliPay.return_url
    if "ali_sms" in json_data:
        json_data["ali_sms"]["key"] = config.AliSms.key
        json_data["ali_sms"]["secrect"] = config.AliSms.secrect

    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)


def set_nacosfiles_config() -> None:
    """
    修改 nacosfiles 目录下的 zip 文件中的配置信息.
    :return: None
    """
    # xx/xx/nacosfiles/
    nacosfiles_path = os.path.join(parent_dir, "nacosfiles")
    for zip_file in os.listdir(nacosfiles_path):
        if not zip_file.endswith(".zip"):
            continue
        # nacosfiles/xxx.zip
        zip_file_path_with_tail = os.path.join(nacosfiles_path, zip_file)
        # nacosfiles/xxx
        zip_file_path = zip_file_path_with_tail[:-4]
        with zipfile.ZipFile(zip_file_path_with_tail, "r") as zip_ref:
            zip_ref.extractall(zip_file_path)
        # 获取 srv_name
        srv_name = zip_file.split("_config")[0]
        # cd nacosfiles/xxx/[dev|pro]
        dirs_name = ["dev", "pro"]
        for dir in dirs_name:
            dir_path = os.path.join(zip_file_path, dir)
            for path in os.listdir(dir_path):
                json_file_path = os.path.join(dir_path, path)
                # 修改 json 文件
                rewrite_json_file(json_file_path, srv_name)
        # 将 nacosfiles/xxx 打包为 nacosfiles/xxx.zip
        new_zip_file_path_with_tail = os.path.join(nacosfiles_path, zip_file)
        with zipfile.ZipFile(new_zip_file_path_with_tail, "w") as zip_ref:
            for root, _, files in os.walk(zip_file_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, zip_file_path)
                    zip_ref.write(file_path, arc_name)
        # 删除 nacosfiles/xxx
        shutil.rmtree(zip_file_path)


def set_nacos_config() -> None:
    """
    修改 backend 中 nacos 配置信息.
    :return: None
    """
    # 修改 services/**/settings.py 中的 nacos 配置信息.
    srvs_list = ["goods_srv", "inventory_srv", "order_srv", "user_srv",
                 "userop_srv"]
    for srv in srvs_list:
        json_file_path = os.path.join(root_dir, "backend", "services", srv,
                                      "config.json")
        json_data = {}
        with open(json_file_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
        json_data["host"] = config.RemoteServer.host
        json_data["nacos"]["host"] = config.DockerServer.host
        json_data["nacos"]["port"] = int(config.Nacos.port)
        json_data["nacos"]["namespace"] = getattr(config.Nacos,
                                                  f"{srv[:-4]}_namespace_id")
        json_data["nacos"]["user"] = config.Nacos.user
        json_data["nacos"]["password"] = config.Nacos.password
        with open(json_file_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

    # 修改 apis/**/config.yaml 中的 nacos 配置信息.
    apis_srv_dict = {"goods_web": "goods", "order_web": "order",
                     "oss_web": "goods", "user_web": "user",
                     "userop_web": "userop"}
    for api in apis_srv_dict.keys():
        yaml_files = ["config-pro.yaml", "config-debug.yaml"]
        api_srv = apis_srv_dict[api]
        for yaml_file in yaml_files:
            yaml_file_path = os.path.join(root_dir, "backend", "apis", api,
                                          yaml_file)
            yaml_data = yaml.load(open(yaml_file_path, "r", encoding="utf-8"),
                                  Loader=yaml.FullLoader)
            yaml_data["host"] = config.DockerServer.host
            yaml_data["port"] = int(config.Nacos.port)
            yaml_data["namespace"] = getattr(config.Nacos,
                                             f"{api_srv}_namespace_id")
            yaml_data["user"] = config.Nacos.user
            yaml_data["password"] = config.Nacos.password
            yaml.dump(yaml_data, open(yaml_file_path, "w", encoding="utf-8"),
                      allow_unicode=True)


def set_jenkins_config() -> None:
    """
    修改 jenkinscfg 目录下的配置文件.
    :return: None
    """
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

    # 修改 ../jenkinscfg/job_pipeline_*.xml 配置文件
    job_names = ["job_pipeline_api", "job_pipeline_srv"]
    for j_name in job_names:
        j_type = j_name.split("_")[-1]
        xml_path = os.path.join(parent_dir, "jenkinscfg", f"{j_name}.xml")
        tree = ET.parse(xml_path)
        root = tree.getroot()
        try:
            sub = root.find("definition") \
                .find("scm") \
                .find("userRemoteConfigs") \
                .find("hudson.plugins.git.UserRemoteConfig")
            sub_url = sub.find("url")
            sub_url.text = getattr(config.Jenkins, f"git_{j_type}_repo")
            sub_credentialsId = sub.find("credentialsId")
            sub_credentialsId.text = config.Jenkins.credential_git_id
        except Exception:
            raise Exception("修改 job_pipeline.xml 文件失败. 请检查配置文件是否正确.")
        tree.write(xml_path, encoding="utf-8", xml_declaration=False)


def modify_jenkinsfile(jenkinsfile_path: str,
                       field_name: str,
                       new_value: str) -> None:
    """
    修改 Jenkinsfile 文件中的字段值.
    :param jenkinsfile_path: Jenkinsfile 文件路径
    :param field_name: 字段名
    :param new_value: 新的字段值
    :return: None
    """
    try:
        # 读取 Jenkinsfile 文件内容
        with open(jenkinsfile_path, "r", encoding="utf-8") as file:
            jenkinsfile_content = file.read()

        # 使用正则表达式找到并替换字段的值
        pattern = r'\b{}\s*:\s*["\'](.+?)["\']'.format(field_name)
        modified_content = re.sub(pattern, '{}: "{}"'.format(
            field_name, new_value), jenkinsfile_content)

        # 将修改后的内容写回到 Jenkinsfile 文件中
        with open(jenkinsfile_path, "w", encoding="utf-8") as file:
            file.write(modified_content)
    except FileNotFoundError:
        print("Jenkinsfile 文件未找到.")
    except Exception as e:
        print("发生错误：", str(e))


def set_jenkinsfile_config() -> None:
    """
    修改 Jenkinsfile 文件中的配置信息.
    将 credentialsId、url、configName 替换为配置文件中的值.
    :return: None
    """
    # 修改 services/**/xx_srv/Jenkinsfile 中的配置信息.
    srvs_list = ["goods_srv", "inventory_srv", "order_srv", "user_srv",
                 "userop_srv"]
    for srv in srvs_list:
        file_path = os.path.join(root_dir, "backend", "services", srv,
                                 "Jenkinsfile")
        modify_jenkinsfile(file_path, "credentialsId",
                           config.Jenkins.credential_git_id)
        modify_jenkinsfile(file_path, "url",
                           config.Jenkins.git_srv_repo)
        modify_jenkinsfile(file_path, "configName",
                           config.RemoteServer.host)

    # 修改 apis/**/xx_web/Jenkinsfile 中的配置信息.
    apis_list = ["goods_web", "order_web", "oss_web", "user_web", "userop_web"]
    for api in apis_list:
        file_path = os.path.join(root_dir, "backend", "apis", api,
                                 "Jenkinsfile")
        modify_jenkinsfile(file_path, "credentialsId",
                           config.Jenkins.credential_git_id)
        modify_jenkinsfile(file_path, "url", config.Jenkins.git_api_repo)
        modify_jenkinsfile(file_path, "configName", config.RemoteServer.host)


def execute() -> None:
    """
    执行函数.
    :return: None
    """
    set_nacosfiles_config()
    set_nacos_config()
    set_jenkins_config()
    set_jenkinsfile_config()


if __name__ == "__main__":
    execute()
