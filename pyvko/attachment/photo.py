from enum import Enum
from typing import Optional

from pyvko.attachment.attachment import Attachment


class Photo(Attachment):
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

    def __init__(self, photo_object: dict) -> None:
        self.__id = photo_object["id"]
        self.__owner_id = photo_object["owner_id"]

        size_mapping = {size["type"]: size["url"] for size in photo_object["sizes"]}
        self.__size_links = {code: size_mapping[code] for code in Photo.Size if code in size_mapping}

    def largest_link(self) -> Optional[str]:
        for code in reversed([i for i in Photo.Size]):
            if code in self.__size_links:
                return self.__size_links[Photo.Size.WIDTH_2560]

        return None

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

    # endregion
