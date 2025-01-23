from abc import abstractmethod, ABC
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict

from vk import API

from pyvko.api_based import ApiMixin, ApiBased
from pyvko.attachment.attachment import Attachment
from pyvko.attachment.attachment_parser import AttachmentParser
from pyvko.aspects.likes import Likes
from pyvko.shared.utils import get_all


@dataclass
class CommentModel:
    text: str
    from_group: int = 0

    attachments: List[Attachment] = None

    def to_request(self):
        request = {}

        if self.text:
            request["message"] = self.text

        if self.from_group != 0:
            request["from_group"] = self.from_group

        if self.attachments:
            request["attachments"] = ",".join([a.to_attach() for a in self.attachments])

        return request


class Comment(ApiBased, Likes):
    @property
    def item_id(self) -> int:
        return self.id

    @property
    def like_object_type(self) -> str:
        return "comment"

    @property
    def owner_id(self) -> int:
        return self.__owner_id

    @property
    def id(self):
        return self.__id

    @property
    def text(self) -> str:
        return self.__text

    @property
    def date(self) -> datetime:
        return self.__date

    def __init__(
            self,
            api: API,
            comment_id: int,
            owner_id: int,
            date: datetime,
            text: str,
            attachments: List[Attachment]
    ) -> None:
        super().__init__(api)

        self.__id = comment_id
        self.__owner_id = owner_id
        self.__date = date
        self.__text = text
        self.__attachments = attachments

    @classmethod
    def from_api_object(cls, api_object: Dict, api: API) -> 'Comment':
        if "attachments" in api_object:
            parser = AttachmentParser.shared()

            attachments = [parser.parse_object(o, api) for o in api_object["attachments"]]
        else:
            attachments = None

        return Comment(
            api=api,
            comment_id=api_object["id"],
            owner_id=api_object["owner_id"],
            date=datetime.fromtimestamp(api_object["date"]),
            text=api_object["text"],
            attachments=attachments
        )


class Comments(ApiMixin, ABC):
    @property
    @abstractmethod
    def post_id(self) -> int:
        pass

    @property
    @abstractmethod
    def owner_id(self) -> int:
        pass

    def add_comment(self, comment: CommentModel) -> Comment:
        add_comment_request = self.get_request(comment.to_request() | {
            "post_id": self.post_id,
            "owner_id": self.owner_id,
        })

        add_comment_response = self.api.wall.createComment(**add_comment_request)

        comment_id = add_comment_response["comment_id"]

        return self.get_comment(comment_id)

    def get_comments(self) -> List[Comment]:
        request = self.get_request({
            "post_id": self.post_id,
            "owner_id": self.owner_id,
            # "count": 10,
        })

        comments_objects = list(get_all(request, self.api.wall.getComments, count_key="current_level_count"))

        comments = [Comment.from_api_object(comments_object, self.api) for comments_object in comments_objects]

        return comments

    def get_comment(self, comment_id: int) -> Comment:
        request = self.get_request({
            "comment_id": comment_id,
            "owner_id": self.owner_id,
            # "count": 10,
        })

        comment_object = self.api.wall.getComment(**request)

        comment = Comment.from_api_object(comment_object["items"][0], self.api)

        return comment
