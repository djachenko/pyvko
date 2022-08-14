from typing import Dict, List

from vk import API

from pyvko.api_based import ApiBased
from pyvko.entities.event import Event
from pyvko.shared.mixins.albums import Albums
from pyvko.shared.mixins.events import Events
from pyvko.shared.mixins.wall import Wall
from pyvko.shared.utils import get_all


class Group(ApiBased, Wall, Albums, Events):
    from pyvko.entities.user import User

    def __init__(self, api: API, group_object: Dict) -> None:
        super().__init__(api)

        self.__group_object = group_object

        self.__id = -group_object["id"]
        self.__name = group_object["name"]
        self.__url = group_object["screen_name"]

    def __str__(self) -> str:
        return f"Group: {self.__name}({self.id})"

    # region Wall

    @property
    def id(self) -> int:
        return self.__id

    # endregion Wall

    @property
    def url(self) -> str:
        return self.__url

    def get_members(self) -> List[User]:
        from pyvko.entities.user import User

        parameters = {
            "group_id": self.id,
            "sort": "time_desc",
            "fields": [
                "online",
            ]
        }

        parameters = self.get_request(parameters)

        users_descriptions = get_all(parameters, self.api.groups.getMembers)

        users = [User(api=self.api, user_object=description) for description in users_descriptions]

        return users

    # region Events

    def create_event(self, title: str) -> Event:
        event = super().create_event(title)

        event.organiser = self.id

        event.save()

        return event

    # endregion Events
