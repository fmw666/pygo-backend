import os
import sys
# append ../ to sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "../"))

from scripts.utils.common import get_nacos_client, get_jenkins_client, get_mysql_cursor


def test_connect() -> bool:
    get_nacos_client()
    get_jenkins_client()
    get_mysql_cursor()
    return True


def execute() -> None:
    print(test_connect())


if __name__ == "__main__":
    execute()
