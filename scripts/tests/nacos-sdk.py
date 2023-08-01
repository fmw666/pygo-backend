from scripts.libs.nacos_sdk import NacosClient


if __name__ == "__main__":
    
    NACOS = {
        "Host": "192.168.200.1",
        "Port": 8848,
        "User": "nacos",
        "Password": "nacos",
    }
    nacos = NacosClient(NACOS["Host"], NACOS["Port"], NACOS["User"], NACOS["Password"])

    # print(nacos.get_configs_namespace_id("068d14d8-6b29-498f-b824-40e92e03a3bd"))
    # print(nacos.import_configs_by_namespace_id("37fc7fc3-ba6f-4194-8a60-baa1e00fefe4", "C:\\Users\\Maovo\\Downloads\\nacos_config_export_20230801205901.zip"))
    