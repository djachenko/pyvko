from functools import lru_cache
from typing import Union

import vk

from pyvko.api_based import ApiBased
from pyvko.config.config import Config
from pyvko.models.active_models import Group, User
from pyvko.shared.mixins import Events, Groups
from pyvko.shared.pure_mixins import EventsImplementation, GroupsImplementation
from pyvko.shared.utils import CaptchedSession, Throttler


class Pyvko(ApiBased):
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
            ]
        })

        user_response = self.api.users.get(**user_request)

        user = User(api=self.api, user_object=user_response[0])

        return user

    def get(self, url: str) -> Union[Group, User, None]:
        request = self.get_request({
            "screen_name": url
        })

        response = self.api.utils.resolveScreenName(**request)

        t = response["type"]

        if t == "group":
            return self.groups.get_group(url)
        elif t == "user":
            return self.get_user(url)

        return None

    @property
    @lru_cache()
    def events(self) -> Events:
        return EventsImplementation(self.api)

    @property
    @lru_cache()
    def groups(self) -> Groups:
        return GroupsImplementation(self.api)
