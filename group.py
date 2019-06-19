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
        request = self.get_request()

        response = self.api.wall.get(**request)

        posts_descriptions = response["items"]

        posts = [Post.from_post_object(description) for description in posts_descriptions]

        return posts

    def add_post(self, post: Post) -> int:
        request = self.get_request({
            "from_group": 1,
            "message": post.text
        })

        result = self.api.wall.post(**request)

        post_id = result["post_id"]

        return post_id

    def delete_post(self, post_id):
        request = self.get_request({
            "post_id": post_id
        })

        self.api.wall.delete(**request)

    def get_request(self, parameters=None) -> dict:
        if parameters is None:
            parameters = {}

        assert "owner_id" not in parameters

        parameters.update({
            "owner_id": -self.id
        })

        return super().get_request(parameters)




