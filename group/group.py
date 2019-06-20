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

    def __get_posts(self, parameters: dict) -> List[Post]:
        request = self.get_request(parameters)

        response = self.api.wall.get(**request)

        posts_descriptions = response["items"]

        posts = [Post.from_post_object(description) for description in posts_descriptions]

        return posts

    def get_posts(self) -> List[Post]:
        return self.__get_posts({})

    def get_scheduled_posts(self) -> List[Post]:
        return self.__get_posts({"filter": "postponed"})

    def __get_post_request(self, post: Post):
        parameters = {
            "from_group": 1
        }

        parameters.update(post.to_request())

        request = self.get_request(parameters)

        return request

    def add_post(self, post: Post) -> int:
        request = self.__get_post_request(post)

        result = self.api.wall.post(**request)

        post_id = result["post_id"]

        return post_id

    def update_post(self, post: Post):
        request = self.__get_post_request(post)

        self.api.wall.edit(**request)

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
