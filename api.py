import vk

import config
from api_based import ApiBased
from user import User


class Api(ApiBased):
    def __init__(self) -> None:
        session = vk.Session(access_token=config.ACCESS_TOKEN)

        api = vk.API(session)

        super().__init__(api)

    def current_user(self) -> User:
        user_response = self.api.users.get(**{"v": 5.92})

        user_id = user_response[0]["id"]

        user = User(api=self.api, user_id=user_id)

        return user
