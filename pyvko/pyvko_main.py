from functools import lru_cache
from urllib.parse import urlparse

import vk

from pyvko.api_based import ApiBased
from pyvko.config.config import Config
from pyvko.entities.event import Event
from pyvko.entities.group import Group
from pyvko.entities.user import User
from pyvko.shared.mixins.events import Events
from pyvko.shared.mixins.groups import Groups
from pyvko.shared.mixins.utils import Utils
from pyvko.shared.pure_mixins import GroupsImplementation, EventsImplementation
from pyvko.shared.utils import Throttler, CaptchedSession


class Pyvko(ApiBased, Utils):
    def __init__(self, config: Config) -> None:
        session = CaptchedSession(access_token=config.access_token)

        api = Throttler(vk.API(session), interval=0.6)

        # noinspection PyTypeChecker
        super().__init__(api)

    def current_user(self) -> User:
        request = self.get_request()

        user_response = self.api.users.get(**request)

        user_id = user_response[0]

        user = User(api=self.api, user_object=user_id)

        return user

    def get_user(self, url: str) -> User:
        user_request = self.get_request({
            "user_ids": [
                url,
            ],
            "fields": [
                "online",
            ],
        })

        user_response = self.api.users.get(**user_request)

        user = User(api=self.api, user_object=user_response[0])

        return user

    def get_by_url(self, url: str) -> Group | User | None:
        name_type = self.resolve_name(url)

        if name_type == "group":
            return self.groups.get_group(url) or self.events.get_event(url)
        elif name_type == "user":
            return self.get_user(url)

        return None

    def get(self, request: str) -> Group | User | Event | None:
        parse_result = urlparse(request)

        qualifier = parse_result.path.split("/")[-1]

        if qualifier.isdecimal():
            qualifier = "id" + qualifier

        prefixes_mapping = {
            "id": self.get_user,
            "event": self.events.get_event,
            "club": self.groups.get_group,
            "public": self.groups.get_group,
            "-": lambda x: self.groups.get_group(x) or self.events.get_event(x)
        }

        for prefix, handler in prefixes_mapping.items():
            if not qualifier.startswith(prefix):
                continue

            id_ = qualifier.removeprefix(prefix)

            return handler(id_)

        return self.get_by_url(qualifier)

    #     full link
    # short link
    # name
    # qualified id
    # signed id

    @property
    @lru_cache()
    def events(self) -> Events:
        return EventsImplementation(self.api)

    @property
    @lru_cache()
    def groups(self) -> Groups:
        return GroupsImplementation(self.api)

    # region utils

    # endregion utils
