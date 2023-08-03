import os
import sys
# append ../ to sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "../"))

from scripts.utils.common import get_nacos_client, get_jenkins_client


def test_connect():
    get_nacos_client()
    get_jenkins_client()
    return True


if __name__ == "__main__":
    print(test_connect())
