from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import List, Dict

from vk import API

from pyvko.api_based import ApiBased, ApiMixin
from pyvko.aspects.comments import Comments
from pyvko.aspects.likes import Likes
from pyvko.aspects.reposts import Reposts
from pyvko.attachment.attachment import Attachment
from pyvko.attachment.attachment_parser import AttachmentParser
from pyvko.attachment.photo import Photo
from pyvko.shared.photos_uploader import WallPhotoUploader, PhotoUploader
from pyvko.shared.utils import get_all


@dataclass
class PostModel:
    text: str = None
    attachments: List[Attachment] = None
    date: datetime = None

    def to_request(self) -> dict:
        request = {}

        if self.text is not None:
            request["message"] = self.text

        if self.attachments is not None:
            request["attachments"] = ",".join([a.to_attach() for a in self.attachments])

        if self.date is not None:
            request["publish_date"] = int(self.date.timestamp())

        return request


class Post(ApiBased, Comments, Likes, Reposts):
    @property
    def like_object_type(self) -> str:
        return "post"

    @property
    def item_id(self) -> int:
        return self.id

    @property
    def post_id(self) -> int:
        return self.id

    @property
    def owner_id(self) -> int:
        return self.__owner_id

    def __init__(self, api: API, owner_id: int, text: str = None, attachments: List[Attachment] = None,
                 date: datetime = None) -> None:
        super().__init__(api)

        if attachments is None:
            attachments = []

        self.date = date
        self.attachments = attachments
        self.id = None
        self.text = text
        self.timer_id = None
        self.__owner_id = owner_id

    def __str__(self) -> str:
        return f"Post: {self.id} | {self.text}"

    @staticmethod
    def from_post_object(post_object: Dict, api: API) -> 'Post':
        if "attachments" in post_object:
            parser = AttachmentParser.shared()

            attachments = [parser.parse_object(o, api) for o in post_object["attachments"]]
        else:
            attachments = None

        post = Post(
            api=api,
            owner_id=post_object["owner_id"],
            text=post_object["text"],
            date=datetime.fromtimestamp(post_object["date"]),
            attachments=attachments,
        )

        post.id = post_object["id"]

        if "postponed_id" in post_object:
            post.timer_id = post_object["postponed_id"]

        return post

    def to_request(self) -> dict:
        request = {}

        if self.id is not None:
            request["post_id"] = self.id

        if self.text is not None:
            request["message"] = self.text

        if self.attachments is not None:
            request["attachments"] = ",".join([a.to_attach() for a in self.attachments])

        if self.date is not None:
            request["publish_date"] = int(self.date.timestamp())

        return request


class Posts(ApiMixin, ABC):
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

    def get_posts(self, *ids: int) -> List[Post]:
        # from pyvko.entities.comment import Post

        if not ids:
            return self.__get_posts({
                "count": 100,
            })

        request = self.get_request({
            "posts": [f"{self.id}_{post_id}" for post_id in ids],
        })

        posts = self.api.wall.getById(**request)["items"]
        posts = [post for post in posts if not post.get("is_deleted", False)]

        return [Post.from_post_object(post, self.api) for post in posts]

    def get_post(self, post_id: int) -> Post | None:
        posts = self.get_posts(post_id)

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
