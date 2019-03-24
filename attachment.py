from enum import Enum, auto

from vk import API

from api_based import ApiBased


class Attachment(ApiBased):
    class Type(Enum):
        PHOTO = auto()

    def __init__(self, api: API) -> None:
        super().__init__(api)

        self.type = Attachment.Type.PHOTO
