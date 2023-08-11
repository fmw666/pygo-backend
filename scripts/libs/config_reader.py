import configparser


class ConfigSection:
    """
    用于将 Config 中 section 封装为类.
    方便使用 config.section.option 的方式获取值.
    """

    def __init__(self,
                 config: configparser.ConfigParser,
                 section: str) -> None:
        """
        初始化方法
        :param config: ConfigParser 对象
        :param section: Config 中名称
        :return: None
        """
        self.config = config
        self.section = section

    def __str__(self) -> str:
        """
        返回 Config 中 section 的所有键值对
        :return: str
        """
        return str(self.config.options(self.section))


class ConfigReader:
    """用于读取 config.ini 文件的类"""

    def __init__(self, path: str) -> None:
        """
        初始化方法
        :param path: config.ini 文件路径
        :return: None
        """
        self.path = path
        self.config = configparser.ConfigParser()
        self.config.read(self.path, encoding="utf-8")

        # 遍历 config.ini 中的所有 section
        for section in self.config.sections():
            # 为每个 section 创建一个 ConfigSection 对象
            cfg_sec = ConfigSection(self.config, section)

            # 将该 section 添加为当前对象的属性 -> config.section
            setattr(self, section, cfg_sec)

            # 遍历 section 中的所有 option，添加为 ConfigSection 对象的属性
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
