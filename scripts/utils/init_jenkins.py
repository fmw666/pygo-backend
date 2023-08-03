import os
import sys
# append ../ to sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "../"))

from scripts.utils.common import get_jenkins_client


jk = get_jenkins_client()

folder_name = "pygo_backend"
jk.create_folder(folder_name=folder_name)

# 获取 ../jenkinscfg/pipeline.xml 配置文件
xml_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "jenkinscfg", "job_pipeline.xml")
xml = open(xml_path, "r", encoding="utf-8").read()

# 创建任务
job_name = "gin-test222"
if jk.job_exists(name=job_name):
    jk.rename_job(from_name=job_name, to_name=f"{job_name}_old")
jk.create_job(name=job_name, config_xml=xml)
