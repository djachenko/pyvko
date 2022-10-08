from abc import abstractmethod, ABC
from pathlib import Path
from typing import Dict, List

from vk import API

from pyvko.api_based import ApiMixin, ApiBased
from pyvko.attachment.attachment import Attachment
from pyvko.attachment.photo import Photo
from pyvko.shared.photos_uploader import AlbumPhotoUploader
from pyvko.shared.utils import get_all


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


class Albums(ApiMixin, ABC):
    @property
    @abstractmethod
    def id(self) -> int:
        pass

    def __get_albums(self, parameters: Dict = None) -> List[Album]:
        request = self.__get_owned_request(parameters)

        result = self.api.photos.getAlbums(**request)

        albums = [Album(self.api, album_object) for album_object in result["items"]]

        return albums

    def get_all_albums(self) -> List[Album]:
        return self.__get_albums()

    def get_album_by_id(self, album_id: int) -> Album:
        albums_list = self.__get_albums({
            "album_ids": [album_id]
        })

        assert len(albums_list) == 1

        return albums_list[0]

    def create_album(self, name: str) -> Album:
        parameters = {
            "title": name,
            "group_id": abs(self.id),
            "upload_by_admins_only": 1
        }

        parameters = self.get_request(parameters)

        response = self.api.photos.createAlbum(**parameters)

        created_album = Album(self.api, response)

        return created_album

    def __get_owned_request(self, parameters: Dict = None) -> dict:
        if parameters is None:
            parameters = {}
        else:
            parameters = parameters.copy()

        assert "owner_id" not in parameters

        parameters.update({
            "owner_id": self.id
        })

        return self.get_request(parameters)
