from typing import List

from vk import API

from pyvko.api_based import ApiBased
from pyvko.attachment.photo import Photo


class Album(ApiBased):
    def __init__(self, api: API, api_object: dict) -> None:
        super().__init__(api)

        self.__name = api_object["title"]
        self.__id = api_object["id"]
        self.__owner_id = api_object["owner_id"]

    @property
    def name(self) -> str:
        return self.__name

    def get_photos(self) -> List[Photo]:
        parameters = {
            "owner_id": self.__owner_id,
            "album_id": self.__id
        }

        photos = []

        while True:
            parameters["offset"] = len(photos)

            request = self.get_request(parameters)

            response = self.api.photos.get(**request)

            photos_descriptions = response["items"]
            photos_count = response["count"]

            photos_chunk = [Photo(photo_object) for photo_object in photos_descriptions]

            photos += photos_chunk

            if photos_count == len(photos):
                break

        return photos
