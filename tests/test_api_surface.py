"""Детектор отвалившихся методов VK API.

VK удаляет методы молча. Проверка опирается на то, что имя метода резолвится
до валидации параметров: несуществующий метод даёт код 3, существующий с
мусорными параметрами — любой другой код (обычно 100).

Зонд передаёт только нечисловые owner_id/group_id. Деструктивные методы
(wall.post, likes.add, photos.createAlbum) требуют дополнительных параметров,
которых зонд не передаёт, поэтому падают на валидации, ничего не изменив.
"""

import pytest
from vk_api.exceptions import ApiError

METHOD_NOT_FOUND = 3

PROBE_PARAMS = {
    "owner_id": "__probe__",
    "group_id": "__probe__",
}

# Убраны из VK API — оставлены как xfail, чтобы поймать возвращение метода.
REMOVED_METHODS = {
    "groups.create": "removed by VK — event creation is broken",
    "groups.edit": "removed by VK — Event.save() is broken",
    "groups.getSettings": "removed by VK — Event.section_state() is broken",
    "likes.add": "removed by VK — Post.like() is broken",
}

# Методы VK, на которые опирается pyvko. Дополнять при добавлении новых вызовов.
USED_METHODS = [
    "groups.create",
    "groups.edit",
    "groups.get",
    "groups.getById",
    "groups.getMembers",
    "groups.getSettings",
    "likes.add",
    "likes.getList",
    "likes.isLiked",
    "photos.createAlbum",
    "photos.get",
    "photos.getAlbums",
    "photos.getUploadServer",
    "photos.getWallUploadServer",
    "photos.makeCover",
    "photos.save",
    "photos.saveWallPhoto",
    "users.get",
    "utils.getShortLink",
    "utils.resolveScreenName",
    "wall.createComment",
    "wall.delete",
    "wall.edit",
    "wall.get",
    "wall.getById",
    "wall.getComment",
    "wall.getComments",
    "wall.getReposts",
    "wall.post",
]


def _probe(api, method: str) -> int | None:
    """Вызывает метод с мусорными параметрами. Возвращает код ошибки или None."""
    target = api

    for part in method.split("."):
        target = getattr(target, part)

    try:
        target(**PROBE_PARAMS)
    except ApiError as error:
        return error.code

    return None


def _method_id(method: str):
    if method in REMOVED_METHODS:
        return pytest.param(method, marks=pytest.mark.xfail(
            strict=True,
            reason=REMOVED_METHODS[method],
        ))

    return method


@pytest.mark.parametrize("method", [_method_id(m) for m in USED_METHODS])
def test_method_exists(pyvko_client, method: str):
    code = _probe(pyvko_client.new_api, method)

    assert code != METHOD_NOT_FOUND, f"VK removed {method}"
