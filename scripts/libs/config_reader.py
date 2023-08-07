import configparser
from typing import Any


class ConfigSection:
    def __init__(self, config, section):
        self.config = config
        self.section = section

    def __str__(self) -> str:
        return str(self.config.options(self.section))


class ConfigReader:
    def __init__(self, path):
        self.path = path
        self.config = configparser.ConfigParser()
        self.config.read(self.path, encoding="utf-8")

        # 遍历 config.ini 中的所有 section，添加到当前对象中为属性
        for section in self.config.sections():
            cfg_sec = ConfigSection(self.config, section)

            setattr(self, section, cfg_sec)
            # 遍历 section 中的所有 option，添加到当前对象中为属性
            for option in self.config.options(section):
                setattr(cfg_sec, option, self.config.get(section, option))
    
    def sections(self):
        return self.config.sections()

    def get(self, section, option):
        return self.config.get(section, option)

    def getint(self, section, option):
        return self.config.getint(section, option)

    def getfloat(self, section, option):
        return self.config.getfloat(section, option)

    def getboolean(self, section, option):
        return self.config.getboolean(section, option)

    def set(self, section, option, value):
        self.config.set(section, option, value)

    def save(self):
        with open(self.path, "w") as configfile:
            self.config.write(configfile)
