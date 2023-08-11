
from utils.common import (get_nacos_client, get_jenkins_client,
                          get_mysql_cursor)


def test_connect() -> bool:
    """
    测试连接.
    :param: None
    :return: bool
    """
    get_nacos_client()
    get_jenkins_client()
    get_mysql_cursor()
    return True


def execute() -> None:
    """
    执行测试连接.
    :param: None
    :return: None
    """
    print(test_connect())


if __name__ == "__main__":
    execute()
