"""
IF db is not exist, create db
"""
import pymysql


class DBInit:
    def __init__(self, host, port, user, password, charset="utf8mb4") -> None:
        conn = pymysql.connect(host=host,
                               port=port,
                               user=user,
                               password=password,
                               charset=charset)
        self.cursor = conn.cursor()

    def create_if_not_exist(self, db_name):
        try:
            sql = (f"CREATE DATABASE IF NOT EXISTS {db_name} DEFAULT "
                   f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            self.cursor.execute(sql)
        except Exception as e:
            raise e
