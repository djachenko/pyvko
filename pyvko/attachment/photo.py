from enum import Enum
from typing import Optional, Dict

from vk import API

from pyvko.api_based import ApiBased
from pyvko.aspects.likes import Likes
from pyvko.attachment.attachment import Attachment
from pyvko.shared.utils import Json


class Photo(ApiBased, Attachment, Likes):
    class Size(str, Enum):
        WIDTH_75 = "s"
        WIDTH_130 = "m",
        WIDTH_604 = "x",
        WIDTH_807 = "y",
        WIDTH_1080 = "z",
        WIDTH_2560 = "w",

    @property
    def id(self) -> int:
        return self.__id

    def __init__(self, api: API, photo_id: int, owner_id: int, size_links: Dict[Size, str], text: str) -> None:
        super().__init__(api)

        self.__id = photo_id
        self.__owner_id = owner_id
        self.__size_links = size_links
        self.__text = text

    def largest_link(self) -> Optional[str]:
        for code in reversed([i for i in Photo.Size]):
            if code in self.__size_links:
                return self.__size_links[code]

        return None

    @property
    def text(self) -> str:
        return self.__text

    # region Attachment

    @property
    def type(self) -> str:
        return "photo"

    @property
    def owner_id(self) -> int:
        return self.__owner_id

    @property
    def media_id(self) -> int:
        return self.__id

    @property
    def like_object_type(self) -> str:
        return "photo"

    @property
    def item_id(self) -> int:
        return self.__id

    @classmethod
    def from_photo_object(cls, api: API, photo_object: Json):

        id_ = photo_object["id"]
        owner_id = photo_object["owner_id"]

        size_mapping = {size["type"]: size["url"] for size in photo_object["sizes"]}
        size_links = {code: size_mapping[code] for code in Photo.Size if code in size_mapping}

        text = photo_object["text"]

        return Photo(api, id_, owner_id, size_links, text)

    # endregion
