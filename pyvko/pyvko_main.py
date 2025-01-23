from urllib.parse import urlparse

from pyvko.api_based import ApiBased
from pyvko.aspects.events import Events, Event
from pyvko.aspects.groups import Groups, Group
from pyvko.aspects.utils import Utils
from pyvko.config.config import Config
from pyvko.entities.user import User
from pyvko.shared.utils import Throttler, CaptchedApi


class Pyvko(ApiBased, Utils, Events, Groups):
    def __init__(self, config: Config) -> None:
        api = Throttler(CaptchedApi(access_token=config.access_token), interval=1)

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
                "screen_name",
            ],
        })

        user_response = self.api.users.get(**user_request)

        user = User(api=self.api, user_object=user_response[0])

        return user

    def get_by_url(self, url: str) -> Group | User | None:
        name_type = self.resolve_name(url)

        if name_type == "group":
            return self.get_group(url) or self.get_event(url)
        elif name_type == "user":
            return self.get_user(url)

        return None

    def get(self, request: str | int) -> Group | User | Event | None:
        request = str(request)

        parse_result = urlparse(request)

        qualifier = parse_result.path.split("/")[-1]

        if qualifier.isdecimal():
            qualifier = "id" + qualifier

        prefixes_mapping = {
            "id": self.get_user,
            "event": self.get_event,
            "club": self.get_group,
            "public": self.get_group,
            "-": lambda x: self.get_group(x) or self.get_event(x)
        }

        for prefix, handler in prefixes_mapping.items():
            if not (qualifier.startswith(prefix) and qualifier.removeprefix(prefix).isdecimal()):
                continue

            id_ = qualifier.removeprefix(prefix)

            return handler(id_)

        return self.get_by_url(qualifier)

    def execute(self, code: str):
        request = self.get_request() | {
            "code": code,
        }

        response = self.api.execute(**request)

        return response

