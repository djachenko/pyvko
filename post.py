import json
from typing import Dict, List

from vk import API

from api_based import ApiBased
from attachment import Attachment


class Post(ApiBased):
    def __init__(self, api: API, post_object: Dict) -> None:
        super().__init__(api)

        self.__object = post_object

        print(json.dumps(post_object, indent=4))

        self.id: int = post_object["id"]
        self.timer_id: int = post_object.get("postponed_id")
        self.attachments: List[Attachment] = []

    def __str__(self) -> str:
        return f"Post: {self.id}|{self.timer_id}"
