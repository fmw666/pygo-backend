import os
import sys
# append ../ to sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "../"))

from scripts.libs.config_reader import ConfigReader


config = ConfigReader("../config.ini")
print(config.Nacos.users_namespace_desc)
