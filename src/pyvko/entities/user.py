from typing import List, Dict, Any

from pyvko.api_based import ApiBased
from pyvko.aspects.events import Event
from pyvko.aspects.groups import Group
from pyvko.aspects.posts import Posts
from pyvko.shared.utils import get_all


class User(ApiBased, Posts):

    @property
    def id(self) -> int:
        return self.__id

    @property
    def first_name(self) -> str:
        return self.__first_name

    @property
    def last_name(self) -> str:
        return self.__last_name

    @property
    def online(self) -> bool:
        return self.__online

    @property
    def url(self) -> str:
        if self.__screen_name:
            return f"https://vk.com/{self.__screen_name}"
        else:
            return f"https://vk.com/id{self.__id}"

    def __init__(self, api: Any, user_object: Dict) -> None:
        super().__init__(api)

        self.__id = user_object["id"]
        self.__first_name = user_object["first_name"]
        self.__last_name = user_object["last_name"]
        self.__online = bool(user_object["online"])
        self.__screen_name = user_object["screen_name"]

    def groups(self) -> List[Group]:
        request = self.get_request({
            "user_id": self.__id,
            "extended": 1,
        })

        groups_response = self.new_api.groups.get(**request)

        groups_objects = groups_response["items"]

        groups = [Group(api=self.new_api, group_object=group_object) for group_object in groups_objects]

        return groups

    def events(self) -> List[Event]:
        request = self.get_request() | {
            "user_id": self.__id,
            "extended": 1,
            "filter": ",".join([
                "events",
            ]),
        }

        response = list(get_all(request, self.new_api.groups.get))

        events = [Event(self.new_api, event, None) for event in response]

        return events