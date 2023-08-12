"""
IF db is not exist, create db
"""
import pymysql


class DBInit:
    def __init__(self, host: str, port: str, user: str, password: str,
                 charset: str = "utf8mb4") -> None:
        """
        获取 mysql cursor
        :param host: mysql host
        :param port: mysql port
        :param user: mysql user
        :param password: mysql password
        :param charset: mysql charset
        :return: None
        """
        conn = pymysql.connect(host=host,
                               port=port,
                               user=user,
                               password=password,
                               charset=charset)
        self.cursor = conn.cursor()

    def create_if_not_exist(self, db_name: str) -> None:
        """
        如果数据库不存在，则创建数据库
        :param db_name: 数据库名称
        :return: None
        """
        try:
            sql = (f"CREATE DATABASE IF NOT EXISTS {db_name} DEFAULT "
                   f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            self.cursor.execute(sql)
        except Exception as e:
            raise e
