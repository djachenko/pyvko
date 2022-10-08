from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict

from pyvko.api_based import ApiMixin
from pyvko.shared.utils import get_all


@dataclass
class Like:
    author_id: int

    @staticmethod
    def from_api_object(o) -> 'Like':
        return Like(author_id=o)


class Likes(ApiMixin, ABC):
    @property
    @abstractmethod
    def type(self) -> str:
        pass

    @property
    @abstractmethod
    def owner_id(self) -> int:
        pass

    @property
    @abstractmethod
    def item_id(self) -> int:
        pass

    def get_likes(self) -> List[Like]:
        request = self.get_request()

        return [Like.from_api_object(i) for i in get_all(request, self.api.likes.getList)]

    def is_liked(self, by: int | None = None) -> bool:
        params = {}

        if by is not None:
            params["user_id"] = by

        request = self.get_request(params)

        response = self.api.likes.isLiked(**request)

        return response["liked"] == 1

    def get_request(self, parameters: Dict = None) -> Dict:
        return super().get_request({
            "type": self.type,
            "owner_id": self.owner_id,
            "item_id": self.item_id
        })
