from abc import ABC

from pyvko.api_based import ApiMixin
from pyvko.entities.group import Group


class Groups(ApiMixin, ABC):
    def get_group(self, url: str) -> Group | None:
        group_request = self.get_request({
            "group_id": url
        })

        group_response = self.api.groups.getById(**group_request)

        group_object = group_response[0]

        if group_object["type"] not in ["page", "group"]:
            return None

        group = Group(api=self.api, group_object=group_object)

        return group
