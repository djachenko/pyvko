from functools import lru_cache

from vk import API

from pyvko.aspects.albums import Album
from pyvko.attachment.attachment import Attachment
from pyvko.attachment.photo import Photo


class StubAttachment(Attachment):
    def __init__(self, type_: str, owner_id: int, media_id: int):
        self.__type = type_
        self.__owner_id = owner_id
        self.__media_id = media_id

    @property
    def type(self) -> str:
        return self.__type

    @property
    def owner_id(self) -> int:
        return self.__owner_id

    @property
    def media_id(self) -> int:
        return self.__media_id


class Link(Attachment):

    def __init__(self, url: str) -> None:
        super().__init__()
        self.__url = url

    @property
    def type(self) -> str:
        pass

    @property
    def owner_id(self) -> int:
        pass

    @property
    def media_id(self) -> int:
        pass

    def to_attach(self) -> str:
        return self.__url


class AttachmentParser:
    @classmethod
    @lru_cache()
    def shared(cls):
        return cls()

    def parse_photo(self, api_object: dict, api: API) -> Photo:
        return Photo.from_photo_object(api, api_object)

    def parse_album(self, api_object: dict, api: API) -> Album:
        return Album(api, api_object)

    def parse_object(self, api_object: dict, api: API) -> Attachment | None:
        if "photo" in api_object:
            return self.parse_photo(api_object["photo"], api)
        elif "album" in api_object:
            return self.parse_album(api_object["album"], api)
        elif "link" in api_object:
            return Link(api_object["link"]["url"])

        # return StubAttachment(
        #     type_=api_object["type"],
        #
        # )

        # video
        # event
        return None
