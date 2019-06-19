from typing import Dict


class Post:
    def __init__(self, text: str) -> None:
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
