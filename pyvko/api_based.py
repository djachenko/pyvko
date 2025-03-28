from abc import abstractmethod
from typing import Dict

from vk import API


class RequestRoot:
    def get_request(self, parameters: Dict = None):
        return parameters or {}


class ApiMixin(RequestRoot):
    @property
    @abstractmethod
    def api(self) -> API:
        pass

    @abstractmethod
    def get_request(self, parameters: Dict = None) -> Dict:
        return super().get_request(parameters)


class ApiBased(RequestRoot):
    __VERSION = 5.199

    def __init__(self, api: API) -> None:
        super().__init__()

        self.__api = api

    @property
    def api(self) -> API:
        return self.__api

    @staticmethod
    def __get_default_object():
        return {
            "v": ApiBased.__VERSION
        }

    def get_request(self, parameters: Dict = None) -> Dict:
        if parameters is None:
            parameters = {}

        assert "v" not in parameters

        request = ApiBased.__get_default_object() | parameters | super().get_request()

        return request
