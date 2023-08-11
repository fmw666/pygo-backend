import requests


headers = {
    "Content-Type": "application/json"
}


def register_http(name: str, id: str, address: str, port: int) -> None:
    """
    注册 http 服务到 consul 中.
    :param name: 服务名称
    :param id: 服务 id
    :param address: 服务地址
    :param port: 服务端口
    :return: None
    """
    url = "http://127.0.0.1:8500/v1/agent/service/register"
    rsp = requests.put(url, headers=headers, json={
        "NAME": name,
        "ID": id,
        "Address": address,
        "Port": port,
        "Tags": ["python", "srv"],
        "Check": {
            "HTTP": f"http://{address}:{port}/health",
            "Interval": "5s",
            "Timeout": "1s",
            "DeregisterCriticalServiceAfter": "15s"
        }
    })

    if rsp.status_code != 200:
        print("register service error")
    else:
        print("register service success")


def register_grpc(name: str, id: str, address: str, port: int) -> None:
    """
    注册 grpc 服务到 consul 中.
    :param name: 服务名称
    :param id: 服务 id
    :param address: 服务地址
    :param port: 服务端口
    :return: None
    """
    url = "http://127.0.0.1:8500/v1/agent/service/register"
    rsp = requests.put(url, headers=headers, json={
        "NAME": name,
        "ID": id,
        "Address": address,
        "Port": port,
        "Tags": ["python", "srv"],
        "Check": {
            "GRPC": f"{address}:{port}",
            "GRPCUseTLS": False,
            "Interval": "5s",
            "Timeout": "1s",
            "DeregisterCriticalServiceAfter": "15s"
        }
    })

    if rsp.status_code != 200:
        print("register service error")
    else:
        print("register service success")


def deregister(service_id: str) -> None:
    """
    从 consul 中注销服务.
    :param service_id: 服务 id
    :return: None
    """
    url = f"http://127.0.0.1:8500/v1/agent/service/deregister/{service_id}"
    rsp = requests.put(url, headers=headers)
    if rsp.status_code != 200:
        print("deregister service error")
    else:
        print("deregister service success")


if __name__ == "__main__":
    # 由于 consul 部署在 docker 中，通过 127.0.0.1 找不到对应的服务，需要使用宿主机的 ip
    # register_http("user-srv", "user-srv", "192.168.200.1", 8021)
    # register_grpc("user-srv", "user-srv", "192.168.200.1", 50051)
    deregister("user-srv")
