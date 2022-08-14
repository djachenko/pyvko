from datetime import datetime
from typing import List, Dict

from vk import API

from pyvko.api_based import ApiBased
from pyvko.attachment.attachment import Attachment
from pyvko.attachment.attachment_parser import AttachmentParser
from pyvko.shared.mixins.comments import Comments


class Post(ApiBased, Comments):

    @property
    def post_id(self) -> int:
        return self.id

    @property
    def owner_id(self) -> int:
        return self.__owner_id

    def __init__(self, api: API, owner_id: int, text: str = None, attachments: List[Attachment] = None,
                 date: datetime = None) -> None:
        super().__init__(api)

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

            attachments = [parser.parse_object(o) for o in post_object["attachments"]]
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
            request["publish_date"] = self.date.timestamp()

        return request
