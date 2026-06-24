from abc import ABC
from typing import Any, Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from pyvko.entities.user import User

from pyvko.api_based import ApiMixin, ApiBased
from pyvko.aspects.albums import Albums
from pyvko.aspects.events import Events, Event
from pyvko.aspects.posts import Posts
from pyvko.entities.user import User
from pyvko.shared.utils import get_all


class Group(ApiBased, Posts, Albums, Events):
    # from pyvko.entities.user import User

    def __init__(self, api: Any, group_object: Dict) -> None:
        super().__init__(api)

        self.__group_object = group_object

        self.__id = -group_object["id"]
        self.__name = group_object["name"]
        self.__url = group_object["screen_name"]

    def __str__(self) -> str:
        return f"Group: {self.__name}({self.id})"

    @property
    def name(self) -> str:
        return self.__name

    # region Wall

    @property
    def id(self) -> int:
        return self.__id

    # endregion Wall

    @property
    def url(self) -> str:
        return self.__url

    def get_members(self) -> List['User']:
        parameters = {
            "group_id": self.id,
            "sort": "time_desc",
            "fields": [
                "online",
            ]
        }

        parameters = self.get_request(parameters)

        users_descriptions = get_all(parameters, self.new_api.groups.getMembers)

        users = [User(api=self.new_api, user_object=description) for description in users_descriptions]

        return users

    # region Events

    def create_event(self, title: str) -> Event:
        event = super().create_event(title)

        event.organiser = self.id

        event.save()

        return event

    # endregion Events


class Groups(ApiMixin, ABC):
    def get_group(self, url: str | int) -> Group | None:
        if isinstance(url, int):
            url = abs(url)

        group_request = self.get_request({
            "group_id": url
        })

        group_response = self.new_api.groups.getById(**group_request)

        group_object = group_response["groups"][0]

        if group_object["type"] not in ["page", "group"]:
            return None

        group = Group(api=self.new_api, group_object=group_object)

        return group
