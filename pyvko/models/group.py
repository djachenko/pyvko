from functools import lru_cache
from pathlib import Path
from typing import List, Dict

from vk import API

from pyvko.api_based import ApiBased
from pyvko.attachment.photo import Photo
from pyvko.models.post import Post
from pyvko.photos.album import Album
from pyvko.photos.photos_uploader import PhotosUploader
from pyvko.models.user import User


class Group(ApiBased):
    def __init__(self, api: API, group_object: Dict = None) -> None:
        super().__init__(api)

        self.__group_object = group_object

        self.id = group_object["id"]
        self.name = group_object["name"]
        self.url = group_object["screen_name"]

    def __str__(self) -> str:
        return f"Group: {self.name}({self.id})"

    def __get_posts(self, parameters: dict) -> List[Post]:
        posts = []

        while True:
            parameters["offset"] = len(posts)

            request = self.__get_owned_request(parameters)

            response = self.api.wall.get(**request)

            posts_descriptions = response["items"]
            posts_count = response["count"]

            posts_chunk = [Post.from_post_object(description) for description in posts_descriptions]

            posts += posts_chunk

            if posts_count == len(posts):
                break

        return posts

    def get_posts(self) -> List[Post]:
        return self.__get_posts({})

    def get_scheduled_posts(self) -> List[Post]:
        return self.__get_posts({"filter": "postponed"})

    def __get_post_request(self, post: Post):
        parameters = {
            "from_group": 1
        }

        parameters.update(post.to_request())

        request = self.__get_owned_request(parameters)

        return request

    def add_post(self, post: Post) -> int:
        request = self.__get_post_request(post)

        result = self.api.wall.post(**request)

        post_id = result["post_id"]

        return post_id

    def update_post(self, post: Post):
        request = self.__get_post_request(post)

        self.api.wall.edit(**request)

    def delete_post(self, post_id):
        request = self.__get_owned_request({
            "post_id": post_id
        })

        self.api.wall.delete(**request)

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

    @lru_cache()
    def __get_wall_uploader(self):
        return PhotosUploader(self.api)

    def upload_photo_to_wall(self, path: Path) -> Photo:
        uploader = self.__get_wall_uploader()

        return uploader.upload_to_wall(self.id, path)

    def get_members(self) -> List[User]:
        request = self.get_request({
            "group_id": self.id,
            "sort": "time_desc",
            "fields": [
                "online",
            ]
        })

        response = self.api.groups.getMembers(**request)

        users = [User(api=self.api, user_object=item) for item in response["items"]]

        return users

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
