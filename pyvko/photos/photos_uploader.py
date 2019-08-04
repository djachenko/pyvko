import json
from pathlib import Path

import requests as requests

from pyvko.api_based import ApiBased
from pyvko.attachment.photo import Photo


class PhotosUploader(ApiBased):
    def get_wall_photo_server(self, group_id: int = None) -> str:
        parameters = {}

        if group_id is not None:
            parameters["group_id"] = group_id

        request = self.get_request(parameters)

        response = self.api.photos.getWallUploadServer(**request)

        return response["upload_url"]

    def get_album_photo_server(self, album_id: int, group_id: int = None) -> str:
        parameters = {
            "album_id": album_id
        }

        if group_id is not None:
            parameters["group_id"] = group_id

        request = self.get_request(parameters)

        response = self.api.photos.getUploadServer(**request)

        return response["upload_url"]

    def upload_to_server(self, server_url: str, path: Path) -> dict:
        data = {
            "photo": path.open("rb")
        }

        response = requests.post(
            url=server_url,
            files=data
        )

        json_response = json.loads(response.text)

        return json_response

    def upload_to_wall(self, group_id: int, path: Path) -> Photo:
        server_url = self.get_wall_photo_server(group_id)

        json_response = self.upload_to_server(server_url, path)

        params = {
            "group_id": group_id
        }

        params.update({name: json_response[name] for name in [
            "photo",
            "server",
            "hash",
        ]})

        request = self.get_request(params)

        photo_response = self.api.photos.saveWallPhoto(**request)

        photo = Photo(photo_response[0])

        return photo

    def upload_to_album(self, album_id: int, group_id: int, path: Path) -> Photo:
        server_url = self.get_album_photo_server(album_id, group_id)

        json_response = self.upload_to_server(server_url, path)

        params = {
            "album_id": album_id,
            "group_id": group_id,
        }

        params.update({name: json_response[name] for name in [
            "photos_list",
            "server",
            "aid",
            "hash",
        ]})

        request = self.get_request(params)

        photo_response = self.api.photos.save(**request)

        photo = Photo(photo_response[0])

        return photo
