from __future__ import annotations

import json
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest
import requests
from vk_api.exceptions import ApiError

from pyvko.api_based import ApiBased
from pyvko.aspects.albums import Album
from pyvko.aspects.comments import CommentModel
from pyvko.aspects.events import Event
from pyvko.aspects.groups import Group
from pyvko.aspects.likes import Like
from pyvko.aspects.posts import Post, PostModel
from pyvko.attachment.attachment_parser import Link
from pyvko.attachment.photo import Photo
from pyvko.entities.user import User
from pyvko.pyvko_main import Pyvko
from pyvko.shared.exceptions import MethodWasDeleted

Response = Any | Callable[[dict[str, Any]], Any]


class FakeMethod:
    def __init__(self, vk: FakeVk, name: str) -> None:
        self.__vk = vk
        self.__name = name

    def __getattr__(self, name: str) -> FakeMethod:
        return FakeMethod(self.__vk, f"{self.__name}.{name}")

    def __call__(self, **params: Any) -> Any:
        return self.__vk.call(self.__name, params)


class FakeVk:
    def __init__(self, responses: dict[str, Response] | None = None) -> None:
        self.responses: dict[str, Response] = responses or {}
        self.calls: list[tuple[str, dict[str, Any]]] = []

    def __getattr__(self, name: str) -> FakeMethod:
        return FakeMethod(self, name)

    def call(self, method: str, params: dict[str, Any]) -> Any:
        self.calls.append((method, params))

        response = self.responses[method]

        if callable(response):
            return response(params)

        return response

    def params(self, method: str) -> dict[str, Any]:
        matching = [params for name, params in self.calls if name == method]

        assert len(matching) == 1, f"{method} called {len(matching)} times"

        return matching[0]


def page(*items: Any) -> dict[str, Any]:
    return {"items": list(items), "count": len(items)}


def access_denied(params: dict[str, Any]) -> Any:
    raise ApiError(None, "groups.getSettings", params, False, {"error_code": 15, "error_msg": "Access denied"})


GROUP_ID = 10

GROUP_OBJECT = {"id": GROUP_ID, "name": "Group", "screen_name": "group", "type": "group"}

USER_OBJECT = {"id": 1, "first_name": "Ivan", "last_name": "Ivanov", "online": 1, "screen_name": "ivan"}

PHOTO_OBJECT = {"id": 3, "owner_id": -GROUP_ID, "sizes": [{"type": "x", "url": "https://photo/x"}], "text": "photo"}

ALBUM_OBJECT = {"id": 5, "owner_id": -GROUP_ID, "title": "Album"}

POST_OBJECT = {"id": 7, "owner_id": -GROUP_ID, "text": "post", "date": 1_700_000_000}

COMMENT_OBJECT = {"id": 9, "owner_id": -GROUP_ID, "text": "comment", "date": 1_700_000_000}

EVENT_OBJECT = {
    "id": 20,
    "name": "Event",
    "screen_name": "event20",
    "type": "event",
    "start_date": 1_700_000_000,
    "finish_date": 1_700_003_600,
    "is_closed": 0,
}

SETTINGS_OBJECT = {
    "public_category": Event.Category.CONCERT.value,
    "main_section": 1,
    "secondary_section": 4,
    "event_object_id": -GROUP_ID,
} | {section.value: Event.SectionState.ENABLED.value for section in Event.Section}


def make_group(vk: FakeVk) -> Group:
    return Group(api=vk, group_object=GROUP_OBJECT)


def make_post(vk: FakeVk) -> Post:
    return Post.from_post_object(POST_OBJECT, vk)


def make_pyvko(vk: FakeVk) -> Pyvko:
    pyvko = Pyvko.__new__(Pyvko)

    ApiBased.__init__(pyvko, vk)

    return pyvko


# region Groups


@pytest.mark.parametrize("group_type", ["group", "page"])
def test_get_group(group_type: str) -> None:
    vk = FakeVk({"groups.getById": {"groups": [GROUP_OBJECT | {"type": group_type}]}})

    group = make_pyvko(vk).get_group(-GROUP_ID)

    assert group is not None
    assert (group.id, group.name, group.url) == (-GROUP_ID, "Group", "group")
    assert vk.params("groups.getById") == {"group_id": GROUP_ID}


def test_get_group_returns_none_for_event() -> None:
    vk = FakeVk({"groups.getById": {"groups": [EVENT_OBJECT]}})

    assert make_pyvko(vk).get_group(20) is None


def test_get_members() -> None:
    vk = FakeVk({"groups.getMembers": page(USER_OBJECT)})

    members = make_group(vk).get_members()

    assert [member.id for member in members] == [USER_OBJECT["id"]]


# endregion Groups

# region Albums


def test_get_all_albums() -> None:
    vk = FakeVk({"photos.getAlbums": page(ALBUM_OBJECT)})

    albums = make_group(vk).get_all_albums()

    assert [(album.id, album.name) for album in albums] == [(5, "Album")]
    assert vk.params("photos.getAlbums") == {"owner_id": -GROUP_ID}


def test_get_album_by_id() -> None:
    vk = FakeVk({"photos.getAlbums": page(ALBUM_OBJECT)})

    album = make_group(vk).get_album_by_id(5)

    assert album is not None
    assert album.id == 5
    assert vk.params("photos.getAlbums") == {"owner_id": -GROUP_ID, "album_ids": [5]}


def test_get_album_by_id_returns_none_when_missing() -> None:
    vk = FakeVk({"photos.getAlbums": page()})

    assert make_group(vk).get_album_by_id(5) is None


def test_create_album() -> None:
    vk = FakeVk({"photos.createAlbum": ALBUM_OBJECT})

    album = make_group(vk).create_album("Album")

    assert album.id == 5
    assert vk.params("photos.createAlbum") == {"title": "Album", "group_id": GROUP_ID, "upload_by_admins_only": 1}


def test_album_get_photos() -> None:
    vk = FakeVk({"photos.get": page(PHOTO_OBJECT)})

    photos = Album(vk, ALBUM_OBJECT).get_photos()

    assert [(photo.id, photo.largest_link()) for photo in photos] == [(3, "https://photo/x")]
    assert vk.params("photos.get") == {"owner_id": -GROUP_ID, "album_id": 5, "offset": 0}


def test_album_attachment() -> None:
    album = Album(FakeVk(), ALBUM_OBJECT)

    assert album.to_attach() == f"album-{GROUP_ID}_5"
    assert album.url == f"https://vk.com/album-{GROUP_ID}_5"


# endregion Albums

# region Posts


def test_get_posts() -> None:
    vk = FakeVk({"wall.get": page(POST_OBJECT)})

    posts = make_group(vk).get_posts()

    assert [(post.id, post.text, post.owner_id) for post in posts] == [(7, "post", -GROUP_ID)]
    assert vk.params("wall.get") == {"count": 100, "owner_id": -GROUP_ID, "offset": 0}


def test_get_posts_by_ids_skips_deleted() -> None:
    deleted = POST_OBJECT | {"id": 8, "is_deleted": True}
    vk = FakeVk({"wall.getById": {"items": [POST_OBJECT, deleted]}})

    posts = make_group(vk).get_posts(7, 8)

    assert [post.id for post in posts] == [7]
    assert vk.params("wall.getById") == {"posts": [f"-{GROUP_ID}_7", f"-{GROUP_ID}_8"]}


@pytest.mark.parametrize(("items", "expected_id"), [([POST_OBJECT], 7), ([], None)])
def test_get_post(items: list[dict[str, Any]], expected_id: int | None) -> None:
    vk = FakeVk({"wall.getById": {"items": items}})

    post = make_group(vk).get_post(7)

    assert (post and post.id) == expected_id


def test_get_scheduled_posts() -> None:
    vk = FakeVk({"wall.get": page(POST_OBJECT | {"postponed_id": 11})})

    posts = make_group(vk).get_scheduled_posts()

    assert [post.timer_id for post in posts] == [11]
    assert vk.params("wall.get")["filter"] == "postponed"


def test_add_post() -> None:
    vk = FakeVk({
        "wall.post": {"post_id": 7},
        "wall.getById": {"items": [POST_OBJECT]},
    })
    model = PostModel(text="post", attachments=[Album(vk, ALBUM_OBJECT)], date=datetime.fromtimestamp(1_800_000_000))

    post = make_group(vk).add_post(model)

    assert post.id == 7
    assert vk.params("wall.post") == {
        "from_group": 1,
        "primary_attachments_mode": "grid",
        "message": "post",
        "attachments": f"album-{GROUP_ID}_5",
        "publish_date": 1_800_000_000,
        "owner_id": -GROUP_ID,
    }


def test_update_post() -> None:
    vk = FakeVk({"wall.edit": 1})
    post = make_post(vk)
    post.text = "edited"

    make_group(vk).update_post(post)

    params = vk.params("wall.edit")

    assert params["post_id"] == 7
    assert params["owner_id"] == -GROUP_ID
    assert params["message"] == "edited"


def test_upload_photo_to_wall(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    photo_path = tmp_path / "photo.jpg"
    photo_path.write_bytes(b"jpeg")

    upload_response = {"photo": "[]", "server": 1, "hash": "hash"}

    class FakeResponse:
        text = json.dumps(upload_response)

    sent_urls: list[str] = []

    def fake_post(url: str, files: dict[str, Any]) -> FakeResponse:
        sent_urls.append(url)

        return FakeResponse()

    monkeypatch.setattr(requests, "post", fake_post)

    vk = FakeVk({
        "photos.getWallUploadServer": {"upload_url": "https://upload.example/wall"},
        "photos.saveWallPhoto": [PHOTO_OBJECT],
    })

    photo = make_group(vk).upload_photo_to_wall(photo_path)

    assert photo.id == 3
    assert sent_urls == ["https://upload.example/wall"]
    assert vk.params("photos.getWallUploadServer") == {"group_id": GROUP_ID}
    assert vk.params("photos.saveWallPhoto") == {"group_id": GROUP_ID} | upload_response


def test_post_parses_attachments() -> None:
    post_object = POST_OBJECT | {"attachments": [
        {"photo": PHOTO_OBJECT},
        {"album": ALBUM_OBJECT},
        {"link": {"url": "https://example.com"}},
    ]}

    post = Post.from_post_object(post_object, FakeVk())

    photo, album, link = post.attachments

    assert isinstance(photo, Photo) and photo.id == 3
    assert isinstance(album, Album) and album.id == 5
    assert isinstance(link, Link) and link.to_attach() == "https://example.com"


# endregion Posts

# region Comments


def test_add_comment() -> None:
    vk = FakeVk({
        "wall.createComment": {"comment_id": 9},
        "wall.getComment": {"items": [COMMENT_OBJECT]},
    })

    comment = make_post(vk).add_comment(CommentModel(text="comment", from_group=GROUP_ID))

    assert (comment.id, comment.text) == (9, "comment")
    assert vk.params("wall.createComment").items() >= {
        "message": "comment",
        "from_group": GROUP_ID,
        "post_id": 7,
        "owner_id": -GROUP_ID,
    }.items()
    assert vk.params("wall.getComment").items() >= {"comment_id": 9, "owner_id": -GROUP_ID}.items()


def test_get_comments() -> None:
    vk = FakeVk({"wall.getComments": {"items": [COMMENT_OBJECT], "count": 5, "current_level_count": 1}})

    comments = make_post(vk).get_comments()

    assert [comment.id for comment in comments] == [9]
    assert vk.params("wall.getComments").items() >= {"post_id": 7, "owner_id": -GROUP_ID, "offset": 0}.items()


# endregion Comments

# region Likes


def test_get_likes() -> None:
    vk = FakeVk({"likes.getList": page(1, 2)})

    post = make_post(vk)

    assert post.get_likes() == [Like(author_id=1), Like(author_id=2)]
    assert vk.params("likes.getList").items() >= {"type": "post", "owner_id": -GROUP_ID, "item_id": 7}.items()


@pytest.mark.parametrize(("likers", "expected"), [((), False), ((1,), True)])
def test_has_likes(likers: tuple[int, ...], expected: bool) -> None:
    vk = FakeVk({"likes.getList": page(*likers)})

    assert make_post(vk).has_likes() == expected


@pytest.mark.parametrize(("liked", "expected"), [(1, True), (0, False)])
def test_is_liked(liked: int, expected: bool) -> None:
    vk = FakeVk({"likes.isLiked": {"liked": liked}})

    assert make_post(vk).is_liked(by=1) == expected
    assert vk.params("likes.isLiked").items() >= {"type": "post", "owner_id": -GROUP_ID, "item_id": 7, "user_id": 1}.items()


def test_like_raises_method_was_deleted() -> None:
    vk = FakeVk()

    with pytest.raises(MethodWasDeleted):
        make_post(vk).like()

    assert vk.calls == []


def test_likes_object_types() -> None:
    vk = FakeVk({"likes.getList": page()})

    comment = make_post(FakeVk({"wall.getComment": {"items": [COMMENT_OBJECT]}})).get_comment(9)
    photo = Photo.from_photo_object(vk, PHOTO_OBJECT)

    assert (comment.like_object_type, comment.item_id) == ("comment", 9)
    assert (photo.like_object_type, photo.item_id) == ("photo", 3)


# endregion Likes

# region Events


def test_get_event() -> None:
    vk = FakeVk({
        "groups.getById": {"groups": [EVENT_OBJECT]},
        "groups.getSettings": SETTINGS_OBJECT,
    })

    event = make_pyvko(vk).get_event("https://vk.com/event20")

    assert event is not None
    assert event.id == -20
    assert event.name == "Event"
    assert event.end_date == datetime.fromtimestamp(1_700_003_600)
    assert event.event_category == Event.Category.CONCERT
    assert event.main_section == Event.Section.PHOTOS
    assert event.secondary_section == Event.Section.VIDEOS
    assert event.section_state(Event.Section.WALL) == Event.SectionState.ENABLED
    assert event.organiser == -GROUP_ID
    assert vk.params("groups.getById")["group_id"] == "20"
    assert vk.params("groups.getSettings")["group_id"] == 20


def test_get_event_without_settings_access() -> None:
    vk = FakeVk({
        "groups.getById": {"groups": [EVENT_OBJECT]},
        "groups.getSettings": access_denied,
    })

    event = make_pyvko(vk).get_event(20)

    assert event is not None
    assert event.event_category is None
    assert event.section_state(Event.Section.WALL) is None


def test_get_event_returns_none_for_group() -> None:
    vk = FakeVk({"groups.getById": {"groups": [GROUP_OBJECT]}})

    assert make_pyvko(vk).get_event(GROUP_ID) is None


# endregion Events

# region User


def test_user_groups() -> None:
    vk = FakeVk({"groups.get": {"items": [GROUP_OBJECT], "count": 1}})

    groups = User(vk, USER_OBJECT).groups()

    assert [group.id for group in groups] == [-GROUP_ID]
    assert vk.params("groups.get") == {"user_id": 1, "extended": 1}


def test_user_events() -> None:
    vk = FakeVk({"groups.get": page(EVENT_OBJECT)})

    events = User(vk, USER_OBJECT).events()

    assert [event.id for event in events] == [-20]
    assert vk.params("groups.get")["filter"] == "events"


@pytest.mark.parametrize(("screen_name", "url"), [("ivan", "https://vk.com/ivan"), ("", "https://vk.com/id1")])
def test_user_url(screen_name: str, url: str) -> None:
    user = User(FakeVk(), USER_OBJECT | {"screen_name": screen_name})

    assert user.url == url


# endregion User

# region Pyvko


def test_current_user() -> None:
    vk = FakeVk({"users.get": [USER_OBJECT]})

    user = make_pyvko(vk).current_user()

    assert (user.id, user.first_name, user.last_name, user.online) == (1, "Ivan", "Ivanov", True)


def test_get_user() -> None:
    vk = FakeVk({"users.get": [USER_OBJECT]})

    user = make_pyvko(vk).get_user("ivan")

    assert user.id == 1
    assert vk.params("users.get") == {"user_ids": ["ivan"], "fields": ["online", "screen_name"]}


def test_resolve_name() -> None:
    vk = FakeVk({"utils.resolveScreenName": {"type": "group", "object_id": GROUP_ID}})

    assert make_pyvko(vk).resolve_name("group") == "group"
    assert vk.params("utils.resolveScreenName") == {"screen_name": "group"}


@pytest.mark.parametrize(("request_", "expected_type"), [
    ("https://vk.com/id1", User),
    ("1", User),
    ("club10", Group),
    ("public10", Group),
    ("-10", Group),
    ("event20", Event),
])
def test_get_by_prefix(request_: str, expected_type: type) -> None:
    vk = FakeVk({
        "users.get": [USER_OBJECT],
        "groups.getById": lambda params: {"groups": [EVENT_OBJECT if params["group_id"] == "20" else GROUP_OBJECT]},
        "groups.getSettings": access_denied,
    })

    assert isinstance(make_pyvko(vk).get(request_), expected_type)


@pytest.mark.parametrize(("name_type", "groups", "expected_type"), [
    ("user", [GROUP_OBJECT], User),
    ("group", [GROUP_OBJECT], Group),
    ("group", [EVENT_OBJECT], Event),
])
def test_get_by_url(name_type: str, groups: list[dict[str, Any]], expected_type: type) -> None:
    vk = FakeVk({
        "utils.resolveScreenName": {"type": name_type},
        "users.get": [USER_OBJECT],
        "groups.getById": {"groups": groups},
        "groups.getSettings": access_denied,
    })

    assert isinstance(make_pyvko(vk).get("https://vk.com/somename"), expected_type)


def test_get_by_url_unknown_type() -> None:
    vk = FakeVk({"utils.resolveScreenName": {"type": "application"}})

    assert make_pyvko(vk).get_by_url("app") is None


def test_execute() -> None:
    vk = FakeVk({"execute": {"result": 1}})

    assert make_pyvko(vk).execute("return 1;") == {"result": 1}
    assert vk.params("execute") == {"code": "return 1;"}


# endregion Pyvko
