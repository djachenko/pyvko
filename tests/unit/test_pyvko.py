from __future__ import annotations

from typing import Any

import pytest

from pyvko.aspects.events import Event
from pyvko.aspects.groups import Group
from pyvko.entities.user import User
from pyvko.pyvko_main import Pyvko
from tests.unit.fake_vk import FakeVk, access_denied
from tests.unit.vk_objects import EVENT_OBJECT, GROUP_ID, GROUP_OBJECT, USER_OBJECT


class TestPyvko:
    def test_current_user(self, vk: FakeVk, pyvko: Pyvko) -> None:
        vk.responses = {
            "users.get": [
                USER_OBJECT,
            ],
        }

        user = pyvko.current_user()

        assert (user.id, user.first_name, user.last_name, user.online) == (1, "Ivan", "Ivanov", True)

    def test_get_user(self, vk: FakeVk, pyvko: Pyvko) -> None:
        vk.responses = {
            "users.get": [
                USER_OBJECT,
            ],
        }

        user = pyvko.get_user("ivan")

        assert user.id == 1
        assert vk.params("users.get") == {
            "user_ids": [
                "ivan",
            ],
            "fields": [
                "online",
                "screen_name",
            ],
        }

    def test_resolve_name(self, vk: FakeVk, pyvko: Pyvko) -> None:
        vk.responses = {
            "utils.resolveScreenName": {
                "type": "group",
                "object_id": GROUP_ID,
            },
        }

        assert pyvko.resolve_name("group") == "group"
        assert vk.params("utils.resolveScreenName") == {
            "screen_name": "group",
        }

    @pytest.mark.parametrize(("request_", "expected_type"), [
        ("https://vk.com/id1", User),
        ("1", User),
        ("club10", Group),
        ("public10", Group),
        ("-10", Group),
        ("event20", Event),
    ])
    def test_get_by_prefix(self, vk: FakeVk, pyvko: Pyvko, request_: str, expected_type: type) -> None:
        def groups_by_id(params: dict[str, Any]) -> dict[str, Any]:
            group_object = EVENT_OBJECT if params["group_id"] == "20" else GROUP_OBJECT

            return {
                "groups": [
                    group_object,
                ],
            }

        vk.responses = {
            "users.get": [
                USER_OBJECT,
            ],
            "groups.getById": groups_by_id,
            "groups.getSettings": access_denied,
        }

        assert isinstance(pyvko.get(request_), expected_type)

    @pytest.mark.parametrize(("name_type", "groups", "expected_type"), [
        ("user", [GROUP_OBJECT], User),
        ("group", [GROUP_OBJECT], Group),
        ("group", [EVENT_OBJECT], Event),
    ])
    def test_get_by_url(
            self,
            vk: FakeVk,
            pyvko: Pyvko,
            name_type: str,
            groups: list[dict[str, Any]],
            expected_type: type,
    ) -> None:
        vk.responses = {
            "utils.resolveScreenName": {
                "type": name_type,
            },
            "users.get": [
                USER_OBJECT,
            ],
            "groups.getById": {
                "groups": groups,
            },
            "groups.getSettings": access_denied,
        }

        assert isinstance(pyvko.get("https://vk.com/somename"), expected_type)

    def test_get_by_url_unknown_type(self, vk: FakeVk, pyvko: Pyvko) -> None:
        vk.responses = {
            "utils.resolveScreenName": {
                "type": "application",
            },
        }

        assert pyvko.get_by_url("app") is None

    def test_execute(self, vk: FakeVk, pyvko: Pyvko) -> None:
        vk.responses = {
            "execute": {
                "result": 1,
            },
        }

        assert pyvko.execute("return 1;") == {
            "result": 1,
        }
        assert vk.params("execute") == {
            "code": "return 1;",
        }
