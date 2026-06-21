import json
from abc import abstractmethod
from functools import cache
from pathlib import Path
from typing import Callable, Dict, Iterable, Any

import requests as requests
from vk_api import VkUpload

from pyvko.api_based import ApiBased
from pyvko.attachment.photo import Photo


class PhotoUploader(ApiBased):
    @property
    @abstractmethod
    def server_provider(self) -> Callable[..., Any]:
        pass

    @property
    @abstractmethod
    def saver(self) -> Callable[..., Any]:
        pass

    @property
    @abstractmethod
    def fields(self) -> Iterable[str]:
        pass

    @abstractmethod
    def get_params(self) -> Dict[str, int]:
        pass

    @property
    @cache
    def uploader(self):
        return VkUpload(self.new_api)

    def __upload_to_server(self, path: Path) -> Dict:
        params = self.get_params()

        request = self.get_request(params)

        response = self.server_provider(**request)

        server_url = response["upload_url"]

        with path.open("rb") as image:
            data = {
                "file1": (path.name, image, "image/jpeg"),
            }

            response = requests.post(
                server_url,
                files=data
            )

        json_response = json.loads(response.text)

        return json_response

    def __save_photo(self, json_response: Dict) -> Photo:
        params = self.get_params().copy()

        params.update({name: json_response[name] for name in self.fields})

        request = self.get_request(params)

        photo_response = self.saver(**request)

        photo = Photo.from_photo_object(self.new_api, photo_response[0])

        return photo

    def upload(self, path: Path) -> Photo:
        while True:
            server_response = self.__upload_to_server(path)

            if server_response.get("photo") or server_response.get("photos_list"):
                break

            print()
            print("No photo, reuploading...", end="")

        photo = self.__save_photo(server_response)

        return photo


class WallPhotoUploader(PhotoUploader):
    def __init__(self, api: Any, group_id: int) -> None:
        super().__init__(api)

        self.__group_id = group_id

    @property
    def server_provider(self) -> Callable[..., Any]:
        return self.new_api.photos.getWallUploadServer

    @property
    def saver(self) -> Callable[..., Any]:
        return self.new_api.photos.saveWallPhoto

    @property
    def fields(self) -> Iterable[str]:
        return [
            "photo",
            "server",
            "hash",
        ]

    def get_params(self) -> Dict[str, int]:
        return {
            "group_id": self.__group_id,
        }


class AlbumPhotoUploader(PhotoUploader):
    def __init__(self, api: Any, album_id: int, group_id: int) -> None:
        super().__init__(api)

        self.__album_id = album_id
        self.__group_id = group_id

    @property
    def server_provider(self) -> Callable[..., Any]:
        return self.new_api.photos.getUploadServer

    @property
    def saver(self) -> Callable[..., Any]:
        return self.new_api.photos.save

    @property
    def fields(self) -> Iterable[str]:
        return [
            "photos_list",
            "server",
            "aid",
            "hash",
        ]

    def get_params(self) -> Dict[str, int]:
        return {
            "album_id": self.__album_id,
            "group_id": self.__group_id,
        }
