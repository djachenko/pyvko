from abc import abstractmethod
from typing import Dict, List

from vk import API

from pyvko.photos.album import Album


class Albums:
    @property
    @abstractmethod
    def api(self) -> API:
        pass

    @property
    @abstractmethod
    def id(self) -> int:
        pass

    @abstractmethod
    def get_request(self, parameters: Dict = None) -> dict:
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
            "group_id": self.id,
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
            "owner_id": -self.id
        })

        return self.get_request(parameters)
