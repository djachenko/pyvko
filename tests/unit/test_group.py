from __future__ import annotations

import pytest

from pyvko.aspects.groups import Group
from pyvko.pyvko_main import Pyvko
from tests.unit.fake_vk import FakeVk, page
from tests.unit.vk_objects import EVENT_OBJECT, GROUP_ID, GROUP_OBJECT, USER_OBJECT


class TestGroups:
    @pytest.mark.parametrize("group_type", [
        "group",
        "page",
    ])
    def test_get_group(self, vk: FakeVk, pyvko: Pyvko, group_type: str) -> None:
        vk.responses = {
            "groups.getById": {
                "groups": [
                    GROUP_OBJECT | {
                        "type": group_type,
                    },
                ],
            },
        }

        group = pyvko.get_group(-GROUP_ID)

        assert group is not None
        assert (group.id, group.name, group.url) == (-GROUP_ID, "Group", "group")
        assert vk.params("groups.getById") == {
            "group_id": GROUP_ID,
        }

    def test_get_group_returns_none_for_event(self, vk: FakeVk, pyvko: Pyvko) -> None:
        vk.responses = {
            "groups.getById": {
                "groups": [
                    EVENT_OBJECT,
                ],
            },
        }

        assert pyvko.get_group(20) is None

    def test_get_members(self, vk: FakeVk, group: Group) -> None:
        vk.responses = {
            "groups.getMembers": page(USER_OBJECT),
        }

        members = group.get_members()

        assert [member.id for member in members] == [USER_OBJECT["id"]]
