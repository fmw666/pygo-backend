"""
1. 创建文件夹，若存在同名文件夹则报错退出.
1. 安装 jenkins 插件.
1. 读取 jenkinscfg 下凭证配置文件信息，在文件夹下创建 jenkins 凭证.
1. 读取 jenkinscfg 下配置文件信息，在文件夹下创建 jenkins 任务.
"""
import os
import json
import requests
import jenkins

import xml.etree.ElementTree as ET

from xml.dom.minidom import parse

from utils.common import get_jenkins_client, config


parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_dir = os.path.dirname(parent_dir)

jenkins_url = f"http://{config.DockerServer.host}:{config.Jenkins.port}"
folder_name = "pygo_backend"
sub_folder_name_api = "go_apis"
sub_folder_name_srv = "py_services"


def get_admin_password() -> str:
    """
    通过 dockerfiles/data/jenkins/secrets/initialAdminPassword 获取 admin 初始化的密码
    :param: None
    :return: admin 初始化的密码
    """
    pswd_file_path = os.path.join(root_dir, "dockerfiles", "data", "jenkins",
                                  "secrets", "initialAdminPassword")
    password = ""
    with open(pswd_file_path, "r") as f:
        password = f.read().strip()

    if password == "":
        raise Exception("获取初始密码失败. 请检查文件路径是否正确. 正确路径：\
                        /var/jenkins_home/secrets/initialAdminPassword")
    return password


def get_crumb(session: requests.Session | None = None,
              auth: tuple | None = None) -> str:
    """
    获取 crumb.
    :param session: requests.Session
    :param auth: tuple
    :return: crumb
    """
    crumb_url = f"{jenkins_url}/crumbIssuer/api/json"
    if session:
        response = session.get(crumb_url)
    else:
        response = requests.get(crumb_url, auth=auth)
    return response.json().get("crumb")


def unlock_jenkins() -> None:
    password = get_admin_password()
    unlock_url = f"http://{config.DockerServer.host}:{config.Jenkins.port}"\
                 f"/j_spring_security_check"
    data = {
        "from": "",
        "j_username": "admin",
        "j_password": password,
    }
    data["json"] = data.copy()
    print(str(data))
    resp = requests.post(unlock_url, data=data)
    print(resp.text)
    print(resp.status_code)


def create_user() -> None:
    password = get_admin_password()
    user_url = f"{jenkins_url}/securityRealm/createAccountByAdmin"
    data = {
        # "username": config.Jenkins.username,
        # "password1": config.Jenkins.password,
        # "password2": config.Jenkins.password,
        "username": "fmw",
        "password1": "123456",
        "password2": "123456",
        "fullname": "",
        "Submit": "",
        "Jenkins-Crumb": get_crumb(auth=("admin", password))
    }
    data["json"] = data.copy()
    resp = requests.post(user_url, data=data, auth=("admin", password))
    print(resp.text)
    print(resp.status_code)


def create_folder(client: jenkins.Jenkins) -> None:
    """
    创建文件夹.
    :param client: jenkins.Jenkins
    :return: None
    """
    # 判断文件夹是否存在（目前 api 不支持文件夹改名）
    if client.job_exists(name=folder_name):
        raise Exception(f"已存在名为 {folder_name} 的 job 或文件夹. 请删除后再试.")

    # 创建文件夹
    client.create_folder(folder_name=folder_name)
    client.create_folder(folder_name=f"{folder_name}/{sub_folder_name_api}")
    client.create_folder(folder_name=f"{folder_name}/{sub_folder_name_srv}")


def request_install_plugin_api(plugin_name: str,
                               plugin_url: str,
                               session: requests.Session) -> requests.Response:
    """
    请求安装插件的 api.
    :param plugin_name: 插件名
    :param plugin_url: 安装插件的 url
    :param session: requests.Session
    :return: requests.Response
    """
    headers = {
        "Content-Type": "text/xml",
        "Jenkins-Crumb": get_crumb(session)
    }
    data = f'<jenkins><install plugin="{plugin_name}"></install></jenkins>'
    response = session.post(plugin_url, data=data, headers=headers)
    return response


def install_plugins() -> None:
    """
    安装插件.
    Localization: Chinese (Simplified), SSH Credentials,\
    Publish Over SSH, Pipeline, Git
    :return: None
    """
    plugin_url = f"{jenkins_url}/pluginManager/installNecessaryPlugins"
    session = requests.Session()
    session.auth = (config.Jenkins.username, config.Jenkins.api_token)

    # "SSH plugin@2.6.1"  don't need
    plugin_names = ["Localization: Chinese (Simplified)@1.0.24",
                    "SSH Credentials Plugin@308.ve4497b_ccd8f4",
                    "Publish Over SSH@1.25", "Pipeline@596.v8c21c963d92d",
                    "git@5.2.0"]
    for plugin_name in plugin_names:
        response = request_install_plugin_api(plugin_name, plugin_url, session)
        # print(f"response.status_code: {response.status_code}")
        retry_times = 3
        while response.status_code == 403 and retry_times > 0:
            response = request_install_plugin_api(plugin_name,
                                                  plugin_url,
                                                  session)
            # print(f"response.status_code: {response.status_code}")
            retry_times -= 1


def create_global_credential() -> None:
    """
    创建全局凭据.
    :return: None
    """
    payload = {
        "": "0",
        "credentials": {
            "scope": "GLOBAL",
            "id": config.Jenkins.credential_ssh_id,
            "username": config.Jenkins.credential_ssh_username,
            "password": config.Jenkins.credential_ssh_password,
            "description": config.Jenkins.credential_ssh_description,
            "stapler-class": ("com.cloudbees.plugins.credentials."
                              "impl.UsernamePasswordCredentialsImpl"),
            "$class": ("com.cloudbees.plugins.credentials.impl."
                       "UsernamePasswordCredentialsImpl")
        }
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    auth = (config.Jenkins.username, config.Jenkins.api_token)
    response = requests.post(f"{jenkins_url}"
                             "/credentials/store/system"
                             "/domain/_/createCredentials",
                             auth=auth,
                             headers=headers,
                             data={"json": json.dumps(payload)})
    if response.status_code != 200:
        print("创建全局凭据失败. 请检查用户名和密码是否正确.")
        print(response.text)


def create_credential(client) -> None:
    """
    创建凭据.
    :param client: jenkins.Jenkins
    :return: None
    """
    # create_global_credential()  # don't need to create global credential

    credential_names = ["credential_git", "credential_ssh"]
    for c_name in credential_names:
        xml_path = os.path.join(parent_dir, "jenkinscfg", f"{c_name}.xml")
        xml = open(xml_path, "r", encoding="utf-8").read()

        xml_id = parse(xml_path) \
            .documentElement \
            .getElementsByTagName("id")[0] \
            .firstChild.data
        if client.credential_exists(name=xml_id, folder_name=folder_name):
            client.delete_credential(name=xml_id, folder_name=folder_name)
        client.create_credential(folder_name=folder_name, config_xml=xml)


def modify_job_xml_scriptPath(xml_path: str, value: str) -> None:
    """
    修改 job_pipeline.xml 文件中的 scriptPath 节点的值.
    :param xml_path: job_pipeline.xml 文件路径
    :param value: scriptPath 节点的值
    :return: None
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    try:
        sub = root.find("definition").find("scriptPath")
        sub.text = value
    except Exception:
        raise Exception("修改 job_pipeline.xml 文件失败. 请检查配置文件是否正确.")
    tree.write(xml_path, encoding="utf-8", xml_declaration=False)


def create_job(client) -> None:
    """
    创建 job.
    :param client: jenkins.Jenkins
    :return: None
    """
    jobs_name_dict = {
        "srv": {
            "folder_name": sub_folder_name_srv,
            "jobs_name": [
                "goods-srv-pipeline", "inventory-srv-pipeline",
                "order-srv-pipeline", "user-srv-pipeline",
                "userop-srv-pipeline"
            ]
        },
        "api": {
            "folder_name": sub_folder_name_api,
            "jobs_name": [
                "goods-web-pipeline", "order-web-pipeline", "oss-web-pipeline",
                "user-web-pipeline", "userop-web-pipeline"
            ]
        }
    }

    for job_type, job_info in jobs_name_dict.items():
        sub_folder = job_info["folder_name"]
        jobs_name = job_info["jobs_name"]

        # 获取 ../jenkinscfg/pipeline.xml 配置文件
        xml_path = os.path.join(parent_dir, "jenkinscfg",
                                f"job_pipeline_{job_type}.xml")

        for job_name in jobs_name:
            # xxx-web-pipeline -> xxx_web,  xxx-srv-pipeline -> xxx_srv
            proj_folder_name = job_name \
                .replace("-pipeline", "").replace("-", "_")
            modify_job_xml_scriptPath(xml_path,
                                      f"{proj_folder_name}/Jenkinsfile")
            xml = open(xml_path, "r", encoding="utf-8").read()

            job_name_with_folder = f"{folder_name}/{sub_folder}/{job_name}"

            # 判断任务是否存在
            if client.job_exists(name=job_name_with_folder):
                # 重命名
                rename_count = 1
                new_job_name = f"{job_name_with_folder}_old"
                while client.job_exists(new_job_name):
                    new_job_name = f"{job_name_with_folder}_old_{rename_count}"
                    rename_count += 1
                client.rename_job(from_name=job_name_with_folder,
                                  to_name=new_job_name)

            # 创建任务
            client.create_job(name=job_name_with_folder, config_xml=xml)


def execute():
    """
    执行函数.
    :return: None
    """
    try:
        client = get_jenkins_client()
    except Exception:
        raise Exception("""连接 Jenkins 失败. 失败原因可能如下:
                        1. Jenkins 安装后还未进行管理台初始化. 请前往 web 管理台进行初始化.
                        2. Jenkins 用户身份认证失败，请确保 config.ini 中 Jenkins """ +
                        """用户已在管理台正确创建.""")
    else:
        create_folder(client)
        install_plugins()
        create_credential(client)
        create_job(client)


if __name__ == "__main__":
    execute()
