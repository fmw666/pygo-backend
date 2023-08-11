
from libs.config_reader import ConfigReader


config = ConfigReader("../config.ini")
print(config.Nacos.users_namespace_desc)
