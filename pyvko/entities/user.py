from typing import List, Dict

from vk import API

from pyvko.api_based import ApiBased
from pyvko.entities.group import Group
from pyvko.shared.mixins.wall import Wall


class User(ApiBased, Wall):

    @property
    def id(self) -> int:
        return self.__id

    def __init__(self, api: API, user_object: Dict) -> None:
        super().__init__(api)

        self.__id = user_object["id"]
        self.__first_name = user_object["first_name"]
        self.__last_name = user_object["last_name"]
        self.__online = user_object["online"]

    @property
    def first_name(self) -> str:
        return self.__first_name

    @property
    def last_name(self) -> str:
        return self.__last_name

    @property
    def online(self) -> bool:
        return self.__online

    def groups(self) -> List[Group]:
        request = self.get_request({
            "user_id": self.__id,
            "extended": 1,
        })

        groups_response = self.api.groups.get(**request)

        groups_objects = groups_response["items"]

        groups = [Group(api=self.api, group_object=group_object) for group_object in groups_objects]

        return groups
