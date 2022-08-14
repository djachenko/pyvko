from abc import abstractmethod, ABC
from functools import lru_cache
from pathlib import Path
from typing import List, Dict, Iterable

from pyvko.api_based import ApiMixin
from pyvko.attachment.photo import Photo
from pyvko.entities.post import Post
from pyvko.models import PostModel
from pyvko.photos.photos_uploader import WallPhotoUploader, PhotoUploader
from pyvko.shared.utils import get_all


class Wall(ApiMixin, ABC):
    @property
    @abstractmethod
    def id(self) -> int:
        pass

    def __get_posts(self, parameters: Dict) -> List[Post]:
        # from pyvko.entities.comment import Post

        parameters = self.__get_owned_request(parameters)

        posts_descriptions = get_all(parameters, self.api.wall.get)

        posts = [Post.from_post_object(description, self.api) for description in posts_descriptions]

        return posts

    def get_posts(self, ids: Iterable[int] | None = None) -> List[Post]:
        # from pyvko.entities.comment import Post

        if ids is None:
            return self.__get_posts({})

        request = self.get_request({
            "posts": [f"{self.id}_{post_id}" for post_id in ids],
        })

        posts = self.api.wall.getById(**request)

        return [Post.from_post_object(post, self.api) for post in posts]

    def get_post(self, post_id: int) -> Post | None:
        posts = self.get_posts([post_id])

        if len(posts) == 0:
            return None
        elif len(posts) == 1:
            return posts[0]
        else:
            assert False

    def get_scheduled_posts(self) -> List[Post]:
        return self.__get_posts({"filter": "postponed"})

    def add_post(self, post: PostModel) -> Post:
        request = self.__get_post_request(post)

        result = self.api.wall.post(**request)

        post_id = result["post_id"]

        created_post = self.get_post(post_id)

        return created_post

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
        # todo: split group and user (no id)
        return WallPhotoUploader(self.api, abs(self.id))

    def upload_photo_to_wall(self, path: Path) -> Photo:
        uploader = self.__get_wall_uploader()

        return uploader.upload(path)

    def __get_post_request(self, post: PostModel | Post):
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
            "owner_id": self.id
        })

        return self.get_request(parameters)
