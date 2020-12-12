from pathlib import Path
from typing import List, Dict

from vk import API

from pyvko.api_based import ApiBased
from pyvko.attachment.attachment import Attachment
from pyvko.attachment.photo import Photo
from pyvko.photos.photos_uploader import AlbumPhotoUploader
from pyvko.shared.downloader import get_all


class Album(ApiBased, Attachment):
    def __init__(self, api: API, api_object: dict) -> None:
        super().__init__(api)

        self.__name = api_object["title"]
        self.__id = api_object["id"]
        self.__owner_id = api_object["owner_id"]

    @property
    def name(self) -> str:
        return self.__name

    @property
    def id(self) -> int:
        return self.__id

    def get_photos(self) -> List[Photo]:
        parameters = self.get_request()

        photos_descriptions = get_all(parameters, self.api.photos.get)

        photos = [Photo(photo_object) for photo_object in photos_descriptions]

        return photos

    def get_request(self, parameters: Dict = None) -> dict:
        parameters = parameters.copy()

        parameters.update({
            "owner_id": self.__owner_id,
            "album_id": self.__id
        })

        return super().get_request(parameters)

    def set_cover(self, cover: Photo):
        request = self.get_request({
            "photo_id": cover.id
        })

        self.api.photos.makeCover(**request)

    def add_photo(self, path: Path) -> Photo:
        uploader = AlbumPhotoUploader(self.api, self.id, -self.__owner_id)

        return uploader.upload(path)

    # region Attachment

    @property
    def type(self) -> str:
        return "album"

    @property
    def owner_id(self) -> int:
        return self.__owner_id

    @property
    def media_id(self) -> int:
        return self.id

    # endregion Attachment
