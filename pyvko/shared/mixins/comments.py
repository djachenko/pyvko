from abc import abstractmethod, ABC
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict

from pyvko.api_based import ApiMixin
from pyvko.attachment.attachment import Attachment
from pyvko.attachment.attachment_parser import AttachmentParser
from pyvko.shared.utils import get_all


@dataclass
class CommentModel:
    text: str
    from_group: bool = False
    # attachments: List[Attachment] = Ni

    def to_request(self):
        request = {}

        if self.text:
            request["message"] = self.text

        if self.from_group:
            request["from_group"] = 1

        return request


@dataclass
class Comment:
    id: int
    date: datetime
    text: str
    attachments: List[Attachment]

    @classmethod
    def from_api_object(cls, api_object: Dict) -> 'Comment':
        if "attachments" in api_object:
            parser = AttachmentParser.shared()

            attachments = [parser.parse_object(o) for o in api_object["attachments"]]
        else:
            attachments = None

        return Comment(
            id=api_object["id"],
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

        comments_objects = list(get_all(request, self.api.wall.getComments))

        comments = [Comment.from_api_object(comments_object) for comments_object in comments_objects]

        return comments

    def get_comment(self, comment_id: int) -> Comment:
        request = self.get_request({
            "comment_id": comment_id,
            "owner_id": self.owner_id,
            # "count": 10,
        })

        comment_object = self.api.wall.getComment(**request)

        comment = Comment.from_api_object(comment_object["items"][0])

        return comment
