from __future__ import annotations

import pytest

from pyvko.entities.user import User
from tests.unit.fake_vk import FakeVk, page
from tests.unit.vk_objects import EVENT_OBJECT, GROUP_ID, GROUP_OBJECT, USER_OBJECT


class TestUser:
    def test_groups(self, vk: FakeVk) -> None:
        vk.responses = {
            "groups.get": {
                "items": [
                    GROUP_OBJECT,
                ],
                "count": 1,
            },
        }

        groups = User(vk, USER_OBJECT).groups()

        assert [group.id for group in groups] == [-GROUP_ID]
        assert vk.params("groups.get") == {
            "user_id": 1,
            "extended": 1,
        }

    def test_events(self, vk: FakeVk) -> None:
        vk.responses = {
            "groups.get": page(EVENT_OBJECT),
        }

        events = User(vk, USER_OBJECT).events()

        assert [event.id for event in events] == [-20]
        assert vk.params("groups.get")["filter"] == "events"

    @pytest.mark.parametrize(("screen_name", "url"), [
        ("ivan", "https://vk.com/ivan"),
        ("", "https://vk.com/id1"),
    ])
    def test_url(self, vk: FakeVk, screen_name: str, url: str) -> None:
        user = User(vk, USER_OBJECT | {
            "screen_name": screen_name,
        })

        assert user.url == url
