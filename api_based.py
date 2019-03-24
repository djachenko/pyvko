from vk import API


class ApiBased:
    def __init__(self, api: API) -> None:
        super().__init__()

        self.__api = api

    @property
    def api(self):
        return self.__api
