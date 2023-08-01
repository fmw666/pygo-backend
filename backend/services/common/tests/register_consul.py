import os
import sys
# append ../ to sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "../"))

from common.register import consul


if __name__ == "__main__":
    register = consul.ConsulRegister("127.0.0.1", 8500)

    # goods_srv_host, goods_srv_port = register.get_host_port(f"Service=='goods-srv'")
    # print(goods_srv_host, goods_srv_port)

    print(register.get_service_host_port("goods-srv"))
