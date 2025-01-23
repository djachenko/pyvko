from abc import ABC, abstractmethod
from typing import Dict, List

from pyvko.api_based import ApiMixin


class Reposts(ApiMixin, ABC):
    __IGNORE_PROFILES = [
        100,
    ]

    __IGNORE_GROUPS = [

    ]

    @property
    def __ignore_groups(self) -> List[int]:
        return Reposts.__IGNORE_GROUPS + [
            abs(self.owner_id),
        ]

    @property
    @abstractmethod
    def owner_id(self) -> int:
        pass

    @property
    @abstractmethod
    def post_id(self) -> int:
        pass

    def get_reposters(self):
        request = self.get_request()
        response = self.api.wall.getReposts(**request)

        profiles = response["profiles"]
        profiles = [profile for profile in profiles if profile["id"] not in Reposts.__IGNORE_PROFILES]

        groups = response["groups"]
        groups = [group for group in groups if group["id"] not in self.__ignore_groups]

        a = 7

    def get_request(self, parameters: Dict = None) -> Dict:
        return super().get_request() | {
            "owner_id": self.owner_id,
            "post_id": self.post_id,
        }

