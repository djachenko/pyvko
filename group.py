from typing import List, Dict

from vk import API

from api_based import ApiBased
from post import Post


class Group(ApiBased):
    def __init__(self, api: API, group_object: Dict = None) -> None:
        super().__init__(api)

        self.__group_object = group_object

        self.id = group_object["id"]
        self.name = group_object["name"]

    def __str__(self) -> str:
        return f"Group: {self.name}({self.id})"

    def posts(self) -> List[Post]:
        posts_response = self.api.wall.get(owner_id=-self.id, v=5.92)
        posts_descriptions = posts_response["items"]

        posts = [Post(api=self.api, post_object=description) for description in posts_descriptions]

        return posts
