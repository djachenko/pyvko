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


def test_vk_rejects_negative_group_id(pyvko_client, test_group):
    api = pyvko_client.new_api

    api.groups.getMembers(group_id=abs(test_group.id), count=1)

    with pytest.raises(ApiError):
        api.groups.getMembers(group_id=test_group.id, count=1)


def test_vk_rejects_positive_owner_id(pyvko_client, test_group):
    api = pyvko_client.new_api

    api.wall.get(owner_id=test_group.id, count=1)

    with pytest.raises(ApiError):
        api.wall.get(owner_id=abs(test_group.id), count=1)


def test_get_members_returns_users(test_group):
    """Регрессия: get_members слал отрицательный group_id и падал на [100]."""
    members = test_group.get_members()

    assert members
    assert all(member.id > 0 for member in members)
