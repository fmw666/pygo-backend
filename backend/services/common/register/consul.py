import random

from common.register import base

import consul


class ConsulRegister(base.Register):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.c = consul.Consul(host=self.host, port=self.port)

    def register(self, name, id, address, port, tags, check) -> bool:
        if check is None:
            check = {
                "GRPC": f"{address}:{port}",
                "GRPCUseTLS": False,
                "Interval": "5s",
                "Timeout": "1s",
                "DeregisterCriticalServiceAfter": "30s"
            }

        return self.c.agent.service.register(name=name, service_id=id, address=address, port=port, tags=tags, check=check)
    
    def deregister(self, service_id):
        return self.c.agent.service.deregister(service_id)

    def get_all_services(self):
        return self.c.agent.services()
    
    def filter_service(self, name):
        services = self.c.agent.services()
        return [v for _, v in services.items() if v["Service"] == name]
    
    def get_service_host_port(self, name):
        services = self.filter_service(name)
        if not services:
            return None, None
        service = random.choice(services)
        return service["Address"], service["Port"]
