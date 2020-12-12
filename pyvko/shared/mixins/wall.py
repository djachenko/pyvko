from abc import abstractmethod
from functools import lru_cache
from pathlib import Path
from typing import Dict, List

from vk import API

from pyvko.attachment.photo import Photo
from pyvko.models.post import Post
from pyvko.photos.photos_uploader import WallPhotoUploader, PhotoUploader
from pyvko.shared.downloader import get_all


class Wall:
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

    def __get_posts(self, parameters: Dict) -> List[Post]:
        parameters = self.__get_owned_request(parameters)

        posts_descriptions = get_all(parameters, self.api.wall.get)

        posts = [Post.from_post_object(description) for description in posts_descriptions]

        return posts

    def get_posts(self) -> List[Post]:
        return self.__get_posts({})

    def get_scheduled_posts(self) -> List[Post]:
        return self.__get_posts({"filter": "postponed"})

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

    @lru_cache()
    def __get_wall_uploader(self) -> PhotoUploader:
        return WallPhotoUploader(self.api, self.id)

    def upload_photo_to_wall(self, path: Path) -> Photo:
        uploader = self.__get_wall_uploader()

        return uploader.upload(path)

    def __get_post_request(self, post: Post):
        parameters = {
            "from_group": 1
        }

        parameters.update(post.to_request())

        request = self.__get_owned_request(parameters)

        return request

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
