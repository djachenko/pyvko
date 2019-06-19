import vk

import config
from api_based import ApiBased
from group import Group
from shared.throttler import Throttler
from user import User


class Api(ApiBased):
    def __init__(self) -> None:
        session = vk.Session(access_token=config.ACCESS_TOKEN)

        api = Throttler(vk.API(session), interval=0.6)

        super().__init__(api)

    def current_user(self) -> User:
        user_response = self.api.users.get(**{"v": 5.92})

        user_id = user_response[0]["id"]

        user = User(api=self.api, user_id=user_id)

        return user

    def get_group(self, url: str) -> Group:
        group_request = self.get_request({
            "group_id": url
        })

        group_response = self.api.groups.getById(**group_request)

        group = Group(api=self.api, group_object=group_response[0])

        return group
