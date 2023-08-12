from typing import List
import random

from common.register import base

import consul


class ConsulRegister(base.Register):
    """Consul register."""

    def __init__(self, host: str, port: str) -> None:
        """
        get a consul client.
        :param host: Consul host.
        :param port: Consul port.
        :return: None
        """
        self.host = host
        self.port = port
        self.c = consul.Consul(host=self.host, port=self.port)

    def register(self, name: str, id: str, address: str, port: int,
                 tags: List[str], check: None | dict) -> bool:
        """
        register service to consul.
        :param name: service name.
        :param id: service id.
        :param address: service address.
        :param port: service port.
        :param tags: service tags.
        :param check: service check.
        :return: True if register success, else False.
        """
        if check is None:
            check = {
                "GRPC": f"{address}:{port}",
                "GRPCUseTLS": False,
                "Interval": "5s",
                "Timeout": "1s",
                "DeregisterCriticalServiceAfter": "30s"
            }

        return self.c.agent.service.register(name=name,
                                             service_id=id,
                                             address=address,
                                             port=port,
                                             tags=tags,
                                             check=check)

    def deregister(self, service_id: str) -> bool:
        """
        deregister service from consul.
        :param service_id: service id.
        :return: True if deregister success, else False.
        """
        return self.c.agent.service.deregister(service_id)

    def get_all_services(self) -> dict:
        """
        get all services from consul.
        :return: all services.
        """
        return self.c.agent.services()

    def filter_service(self, name: str) -> list:
        """
        filter services by name.
        :param name: service name.
        :return: list of services.
        """
        services = self.get_all_services()
        return [v for _, v in services.items() if v["Service"] == name]

    def get_service_host_port(self, name: str) -> tuple:
        """
        get a random service host and port by name.
        :param name: service name.
        :return: host and port.
        """
        services = self.filter_service(name)
        if not services:
            return None, None
        service = random.choice(services)
        return service["Address"], service["Port"]
