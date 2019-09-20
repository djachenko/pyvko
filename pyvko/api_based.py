from typing import Dict

from vk import API


class ApiBased:
    __VERSION = 5.92

    def __init__(self, api) -> None:
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

    def get_request(self, parameters: Dict = None) -> dict:
        if parameters is None:
            parameters = {}

        assert "v" not in parameters

        request = ApiBased.__get_default_object()

        request.update(parameters)

        return request
