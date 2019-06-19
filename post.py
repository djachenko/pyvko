from typing import Dict, List

from attachment import Attachment


class Post:
    def __init__(self, text: str = None, attachments: List[Attachment] = None) -> None:
        self.attachments = attachments
        self.id = -1
        self.text = text

        # self.id: int = post_object["id"]
        # self.timer_id: int = post_object.get("postponed_id")
        # self.attachments: List[Attachment] = []
        # self.message = post_object["message"]

    def __str__(self) -> str:
        return f"Post: {self.id}|{self.text}"

    @staticmethod
    def from_post_object(post_object: Dict) -> 'Post':
        post = Post(
            text=post_object["text"],
        )

        post.id = post_object["id"]

        return post

    def to_request(self) -> dict:
        request = {}

        if self.id != -1:
            request["post_id"] = self.id

        if self.text is not None:
            request["text"] = self.text

        if self.attachments is not None:
            request["attachments"] = ",".join([a.to_attach() for a in self.attachments])

        return request
