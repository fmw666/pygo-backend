import os
import sys

from xml.dom.minidom import parse

import jenkins


jk = jenkins.Jenkins(url="http://192.168.200.1:9080", username="root", password="123456")

# 创建任务
folder_name = "pygo_backend"

# 判断文件夹是否存在（目前 api 不支持文件夹改名）
if jk.job_exists(name=folder_name):
    print(f"已存在名为 {folder_name} 的 job 或文件夹. 请删除后再试.")
    sys.exit(1)

# 创建文件夹
jk.create_folder(folder_name=folder_name)

# 创建凭证
credential_names = ["credential_git", "credential_ssh"]
for c_name in credential_names:
    xml_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "jenkinscfg", f"{c_name}.xml")
    xml = open(xml_path, "r", encoding="utf-8").read()

    xml_id = parse(xml_path).documentElement.getElementsByTagName("id")[0].firstChild.data
    if jk.credential_exists(name=xml_id, folder_name=folder_name):
        jk.delete_credential(name=xml_id, folder_name=folder_name)
    jk.create_credential(folder_name=folder_name, config_xml=xml)

# 创建任务
jobs_name = ["goods-web-pipeline", "goods-srv-pipeline",]

# 获取 ../jenkinscfg/pipeline.xml 配置文件
xml_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "jenkinscfg", "job_pipeline.xml")
xml = open(xml_path, "r", encoding="utf-8").read()

for job_name in jobs_name:
    job_name_with_folder = f"{folder_name}/{job_name}"

    # 判断任务是否存在
    if jk.job_exists(name=job_name_with_folder):
        # 重命名
        rename_count = 1
        new_job_name = f"{job_name_with_folder}_old"
        while jk.job_exists(new_job_name):
            new_job_name = f"{job_name_with_folder}_old_{rename_count}"
            rename_count += 1
        jk.rename_job(from_name=job_name_with_folder, to_name=new_job_name)

    # 创建任务
    jk.create_job(name=job_name_with_folder, config_xml=xml)

    # # 构建任务
    # jk.build_job(name=job_name_with_folder)


# # 安装插件
# # jk.install_plugin(name="GitHub API")
# # print(jk.get_plugins())

