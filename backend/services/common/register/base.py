from typing import List

import abc


class Register(metaclass=abc.ABCMeta):
    """Register interface."""

    @abc.abstractmethod
    def register(self, name: str, id: str, address: str, port: int,
                 tags: List[str], check: None | dict) -> bool:
        pass

    @abc.abstractmethod
    def deregister(self, service_id: str) -> bool:
        pass

    @abc.abstractmethod
    def get_all_services(self) -> dict:
        pass

    @abc.abstractmethod
    def filter_service(self, name: str) -> list:
        pass
