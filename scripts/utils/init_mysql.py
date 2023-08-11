"""
1. 通过 pymysql 连接 mysql，并创建数据库.
2. 通过运行 `python backend/services/xxx_srv/model/models.py` 来创建表和初始化表记录.
"""
import os

from utils.common import get_mysql_cursor, config


parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_dir = os.path.dirname(parent_dir)


def create_db() -> None:
    """
    创建数据库.
    :param: None
    :return: None
    """
    cursor = get_mysql_cursor()
    try:
        dbs_name = [config.Mysql.goods_srv_db, config.Mysql.order_srv_db,
                    config.Mysql.inventory_srv_db, config.Mysql.user_srv_db,
                    config.Mysql.userop_srv_db]
        for db_name in dbs_name:
            sql = (f"CREATE DATABASE IF NOT EXISTS {db_name} DEFAULT CHARACTER"
                   f" SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            cursor.execute(sql)
    except Exception as e:
        cursor.close()
        raise Exception(f"create db error: {e}")
    finally:
        cursor.close()


def create_table_and_exec_sql() -> None:
    """
    通过运行 `python backend/services/xxx_srv/model/models.py` 来创建表和初始化表记录.
    :param: None
    :return: None
    """
    srvs_list = ["goods_srv", "inventory_srv", "order_srv", "user_srv",
                 "userop_srv"]

    for srv in srvs_list:
        # find pkg
        py_file_path = os.path.join(root_dir, "backend", "services", srv,
                                    "model", "models.py")
        if not os.path.exists(py_file_path):
            raise FileNotFoundError(f"not found {py_file_path}")
        os.system(f"python {py_file_path}")


def execute() -> None:
    """
    执行创建数据库和表.
    :param: None
    :return: None
    """
    create_db()
    create_table_and_exec_sql()


if __name__ == "__main__":
    execute()
