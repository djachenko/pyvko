"""Фиксация знаковой конвенции идентификаторов сообщества.

VK различает два представления одного и того же сообщества:

    group_id  — положительный (183637090)
    owner_id  — отрицательный (-183637090)

pyvko хранит `Group.id` в owner_id-форме, то есть отрицательным, и приводит
к положительному через `abs()` там, где VK ждёт group_id. Путаница знаков
даёт не пустой результат, а ошибку API, причём разную: неверный group_id —
[100], положительный owner_id — [18], потому что VK трактует его как id
пользователя.

Тесты фиксируют это на живом API. Если VK поменяет конвенцию или pyvko
перестанет её соблюдать — упадут.
"""

import pytest
from vk_api.exceptions import ApiError


def test_group_id_is_negative(test_group):
    assert test_group.id < 0


def test_event_id_is_negative(test_event):
    assert test_event.id < 0


def test_get_group_normalises_sign(pyvko_client, test_group):
    positive = pyvko_client.get_group(abs(test_group.id))
    negative = pyvko_client.get_group(test_group.id)

    assert positive is not None
    assert negative is not None
    assert positive.id == negative.id == test_group.id


_GROUP_ID_METHODS = [
    pytest.param(
        "groups.getMembers",
        {
            "count": 1,
        },
        id="groups.getMembers",
    ),
    pytest.param("groups.getById", {}, id="groups.getById"),
    pytest.param("photos.getWallUploadServer", {}, id="photos.getWallUploadServer"),
]

_OWNER_ID_METHODS = [
    pytest.param(
        "wall.get",
        {
            "count": 1,
        },
        id="wall.get",
    ),
    pytest.param(
        "photos.get",
        {
            "album_id": "wall",
            "count": 1,
        },
        id="photos.get",
    ),
    pytest.param(
        "photos.getAlbums",
        {
            "count": 1,
        },
        id="photos.getAlbums",
    ),
]


def _call(api, method: str, **params):
    target = api

    for part in method.split("."):
        target = getattr(target, part)

    return target(**params)


@pytest.mark.parametrize(("method", "params"), _GROUP_ID_METHODS)
class TestGroupIdIsPositive:
    def test_accepts_positive(self, pyvko_client, test_group, method, params):
        _call(pyvko_client.new_api, method, group_id=abs(test_group.id), **params)

    def test_rejects_negative(self, pyvko_client, test_group, method, params):
        with pytest.raises(ApiError):
            _call(pyvko_client.new_api, method, group_id=test_group.id, **params)


@pytest.mark.parametrize(("method", "params"), _OWNER_ID_METHODS)
class TestOwnerIdIsNegative:
    def test_accepts_negative(self, pyvko_client, test_group, method, params):
        _call(pyvko_client.new_api, method, owner_id=test_group.id, **params)

    def test_rejects_positive(self, pyvko_client, test_group, method, params):
        with pytest.raises(ApiError):
            _call(pyvko_client.new_api, method, owner_id=abs(test_group.id), **params)


def test_get_members_returns_users(test_group):
    """Регрессия: get_members слал отрицательный group_id и падал на [100]."""
    members = test_group.get_members()

    assert members
    assert all(member.id > 0 for member in members)
