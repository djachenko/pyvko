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
from pyvko.shared.photos_uploader import AlbumPhotoUploader

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
    def __init__(self) -> None:
        self.responses: dict[str, Response] = {}
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
    return {
        "items": list(items),
        "count": len(items),
    }


def access_denied(params: dict[str, Any]) -> Any:
    raise ApiError(None, "groups.getSettings", params, False, {
        "error_code": 15,
        "error_msg": "Access denied",
    })


_GROUP_ID = 10

_GROUP_OBJECT = {
    "id": _GROUP_ID,
    "name": "Group",
    "screen_name": "group",
    "type": "group",
}

_USER_OBJECT = {
    "id": 1,
    "first_name": "Ivan",
    "last_name": "Ivanov",
    "online": 1,
    "screen_name": "ivan",
}

_PHOTO_OBJECT = {
    "id": 3,
    "owner_id": -_GROUP_ID,
    "sizes": [
        {
            "type": "x",
            "url": "https://photo/x",
        },
    ],
    "text": "photo",
}

_ALBUM_OBJECT = {
    "id": 5,
    "owner_id": -_GROUP_ID,
    "title": "Album",
}

_POST_OBJECT = {
    "id": 7,
    "owner_id": -_GROUP_ID,
    "text": "post",
    "date": 1_700_000_000,
}

_COMMENT_OBJECT = {
    "id": 9,
    "owner_id": -_GROUP_ID,
    "text": "comment",
    "date": 1_700_000_000,
}

_EVENT_OBJECT = {
    "id": 20,
    "name": "Event",
    "screen_name": "event20",
    "type": "event",
    "start_date": 1_700_000_000,
    "finish_date": 1_700_003_600,
    "is_closed": 0,
}

_SETTINGS_OBJECT = {
    "public_category": Event.Category.CONCERT.value,
    "main_section": 1,
    "secondary_section": 4,
    "event_object_id": -_GROUP_ID,
} | {section.value: Event.SectionState.ENABLED.value for section in Event.Section}


@pytest.fixture
def vk() -> FakeVk:
    return FakeVk()


@pytest.fixture
def group(vk: FakeVk) -> Group:
    return Group(api=vk, group_object=_GROUP_OBJECT)


@pytest.fixture
def post(vk: FakeVk) -> Post:
    return Post.from_post_object(_POST_OBJECT, vk)


@pytest.fixture
def pyvko(vk: FakeVk) -> Pyvko:
    client = Pyvko.__new__(Pyvko)

    ApiBased.__init__(client, vk)

    return client


class TestGroups:
    @pytest.mark.parametrize("group_type", [
        "group",
        "page",
    ])
    def test_get_group(self, vk: FakeVk, pyvko: Pyvko, group_type: str) -> None:
        vk.responses = {
            "groups.getById": {
                "groups": [
                    _GROUP_OBJECT | {
                        "type": group_type,
                    },
                ],
            },
        }

        group = pyvko.get_group(-_GROUP_ID)

        assert group is not None
        assert (group.id, group.name, group.url) == (-_GROUP_ID, "Group", "group")
        assert vk.params("groups.getById") == {
            "group_id": _GROUP_ID,
        }

    def test_get_group_returns_none_for_event(self, vk: FakeVk, pyvko: Pyvko) -> None:
        vk.responses = {
            "groups.getById": {
                "groups": [
                    _EVENT_OBJECT,
                ],
            },
        }

        assert pyvko.get_group(20) is None

    def test_get_members(self, vk: FakeVk, group: Group) -> None:
        vk.responses = {
            "groups.getMembers": page(_USER_OBJECT),
        }

        members = group.get_members()

        assert [member.id for member in members] == [_USER_OBJECT["id"]]


class TestAlbums:
    def test_get_all_albums(self, vk: FakeVk, group: Group) -> None:
        vk.responses = {
            "photos.getAlbums": page(_ALBUM_OBJECT),
        }

        albums = group.get_all_albums()

        assert [(album.id, album.name) for album in albums] == [(5, "Album")]
        assert vk.params("photos.getAlbums") == {
            "owner_id": -_GROUP_ID,
        }

    def test_get_album_by_id(self, vk: FakeVk, group: Group) -> None:
        vk.responses = {
            "photos.getAlbums": page(_ALBUM_OBJECT),
        }

        album = group.get_album_by_id(5)

        assert album is not None
        assert album.id == 5
        assert vk.params("photos.getAlbums") == {
            "owner_id": -_GROUP_ID,
            "album_ids": [5],
        }

    def test_get_album_by_id_returns_none_when_missing(self, vk: FakeVk, group: Group) -> None:
        vk.responses = {
            "photos.getAlbums": page(),
        }

        assert group.get_album_by_id(5) is None

    def test_create_album(self, vk: FakeVk, group: Group) -> None:
        vk.responses = {
            "photos.createAlbum": _ALBUM_OBJECT,
        }

        album = group.create_album("Album")

        assert album.id == 5
        assert vk.params("photos.createAlbum") == {
            "title": "Album",
            "group_id": _GROUP_ID,
            "upload_by_admins_only": 1,
        }

    def test_get_photos(self, vk: FakeVk) -> None:
        vk.responses = {
            "photos.get": page(_PHOTO_OBJECT),
        }

        photos = Album(vk, _ALBUM_OBJECT).get_photos()

        assert [(photo.id, photo.largest_link()) for photo in photos] == [(3, "https://photo/x")]
        assert vk.params("photos.get") == {
            "owner_id": -_GROUP_ID,
            "album_id": 5,
            "offset": 0,
        }

    def test_add_photos(self, vk: FakeVk, monkeypatch: pytest.MonkeyPatch) -> None:
        uploads: list[tuple[Any, int, list[Path]]] = []

        def fake_upload_many(uploader: AlbumPhotoUploader, paths: list[Path]) -> list[Photo]:
            uploads.append((uploader.new_api, uploader.get_params()["group_id"], paths))

            return [Photo.from_photo_object(vk, _PHOTO_OBJECT)]

        monkeypatch.setattr(AlbumPhotoUploader, "upload_many", fake_upload_many)

        photo = Album(vk, _ALBUM_OBJECT).add_photo(Path("photo.jpg"))

        assert photo.id == 3
        assert uploads == [(vk, _GROUP_ID, [Path("photo.jpg")])]

    def test_attachment(self, vk: FakeVk) -> None:
        album = Album(vk, _ALBUM_OBJECT)

        assert album.to_attach() == f"album-{_GROUP_ID}_5"
        assert album.url == f"https://vk.com/album-{_GROUP_ID}_5"


class TestPosts:
    def test_get_posts(self, vk: FakeVk, group: Group) -> None:
        vk.responses = {
            "wall.get": page(_POST_OBJECT),
        }

        posts = group.get_posts()

        assert [(post.id, post.text, post.owner_id) for post in posts] == [(7, "post", -_GROUP_ID)]
        assert vk.params("wall.get") == {
            "count": 100,
            "owner_id": -_GROUP_ID,
            "offset": 0,
        }

    def test_get_posts_by_ids_skips_deleted(self, vk: FakeVk, group: Group) -> None:
        deleted = _POST_OBJECT | {
            "id": 8,
            "is_deleted": True,
        }
        vk.responses = {
            "wall.getById": {
                "items": [
                    _POST_OBJECT,
                    deleted,
                ],
            },
        }

        posts = group.get_posts(7, 8)

        assert [post.id for post in posts] == [7]
        assert vk.params("wall.getById") == {
            "posts": [
                f"-{_GROUP_ID}_7",
                f"-{_GROUP_ID}_8",
            ],
        }

    @pytest.mark.parametrize(("items", "expected_id"), [
        ([_POST_OBJECT], 7),
        ([], None),
    ])
    def test_get_post(self, vk: FakeVk, group: Group, items: list[dict[str, Any]], expected_id: int | None) -> None:
        vk.responses = {
            "wall.getById": {
                "items": items,
            },
        }

        post = group.get_post(7)

        assert (post and post.id) == expected_id

    def test_get_scheduled_posts(self, vk: FakeVk, group: Group) -> None:
        vk.responses = {
            "wall.get": page(_POST_OBJECT | {
                "postponed_id": 11,
            }),
        }

        posts = group.get_scheduled_posts()

        assert [post.timer_id for post in posts] == [11]
        assert vk.params("wall.get")["filter"] == "postponed"

    def test_add_post(self, vk: FakeVk, group: Group) -> None:
        vk.responses = {
            "wall.post": {
                "post_id": 7,
            },
            "wall.getById": {
                "items": [
                    _POST_OBJECT,
                ],
            },
        }
        model = PostModel(
            text="post",
            attachments=[Album(vk, _ALBUM_OBJECT)],
            date=datetime.fromtimestamp(1_800_000_000),
        )

        post = group.add_post(model)

        assert post.id == 7
        assert vk.params("wall.post") == {
            "from_group": 1,
            "primary_attachments_mode": "grid",
            "message": "post",
            "attachments": f"album-{_GROUP_ID}_5",
            "publish_date": 1_800_000_000,
            "owner_id": -_GROUP_ID,
        }

    def test_update_post(self, vk: FakeVk, group: Group, post: Post) -> None:
        vk.responses = {
            "wall.edit": 1,
        }
        post.text = "edited"

        group.update_post(post)

        params = vk.params("wall.edit")

        assert params["post_id"] == 7
        assert params["owner_id"] == -_GROUP_ID
        assert params["message"] == "edited"

    def test_upload_photo_to_wall(
            self,
            vk: FakeVk,
            group: Group,
            tmp_path: Path,
            monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        photo_path = tmp_path / "photo.jpg"
        photo_path.write_bytes(b"jpeg")

        upload_response = {
            "photo": "[]",
            "server": 1,
            "hash": "hash",
        }

        class FakeResponse:
            text = json.dumps(upload_response)

        sent_urls: list[str] = []

        def fake_post(url: str, files: dict[str, Any]) -> FakeResponse:
            sent_urls.append(url)

            return FakeResponse()

        monkeypatch.setattr(requests, "post", fake_post)

        vk.responses = {
            "photos.getWallUploadServer": {
                "upload_url": "https://upload.example/wall",
            },
            "photos.saveWallPhoto": [
                _PHOTO_OBJECT,
            ],
        }

        photo = group.upload_photo_to_wall(photo_path)

        assert photo.id == 3
        assert sent_urls == ["https://upload.example/wall"]
        assert vk.params("photos.getWallUploadServer") == {
            "group_id": _GROUP_ID,
        }
        assert vk.params("photos.saveWallPhoto") == {
            "group_id": _GROUP_ID,
        } | upload_response

    def test_parses_attachments(self, vk: FakeVk) -> None:
        post_object = _POST_OBJECT | {
            "attachments": [
                {
                    "photo": _PHOTO_OBJECT,
                },
                {
                    "album": _ALBUM_OBJECT,
                },
                {
                    "link": {
                        "url": "https://example.com",
                    },
                },
            ],
        }

        post = Post.from_post_object(post_object, vk)

        photo, album, link = post.attachments

        assert isinstance(photo, Photo) and photo.id == 3
        assert isinstance(album, Album) and album.id == 5
        assert isinstance(link, Link) and link.to_attach() == "https://example.com"


class TestComments:
    def test_add_comment(self, vk: FakeVk, post: Post) -> None:
        vk.responses = {
            "wall.createComment": {
                "comment_id": 9,
            },
            "wall.getComment": {
                "items": [
                    _COMMENT_OBJECT,
                ],
            },
        }

        comment = post.add_comment(CommentModel(text="comment", from_group=_GROUP_ID))

        assert (comment.id, comment.text) == (9, "comment")
        assert vk.params("wall.createComment").items() >= {
            "message": "comment",
            "from_group": _GROUP_ID,
            "post_id": 7,
            "owner_id": -_GROUP_ID,
        }.items()
        assert vk.params("wall.getComment").items() >= {
            "comment_id": 9,
            "owner_id": -_GROUP_ID,
        }.items()

    def test_get_comments(self, vk: FakeVk, post: Post) -> None:
        vk.responses = {
            "wall.getComments": {
                "items": [
                    _COMMENT_OBJECT,
                ],
                "count": 5,
                "current_level_count": 1,
            },
        }

        comments = post.get_comments()

        assert [comment.id for comment in comments] == [9]
        assert vk.params("wall.getComments").items() >= {
            "post_id": 7,
            "owner_id": -_GROUP_ID,
            "offset": 0,
        }.items()


class TestLikes:
    def test_get_likes(self, vk: FakeVk, post: Post) -> None:
        vk.responses = {
            "likes.getList": page(1, 2),
        }

        assert post.get_likes() == [Like(author_id=1), Like(author_id=2)]
        assert vk.params("likes.getList").items() >= {
            "type": "post",
            "owner_id": -_GROUP_ID,
            "item_id": 7,
        }.items()

    @pytest.mark.parametrize(("likers", "expected"), [
        ((), False),
        ((1,), True),
    ])
    def test_has_likes(self, vk: FakeVk, post: Post, likers: tuple[int, ...], expected: bool) -> None:
        vk.responses = {
            "likes.getList": page(*likers),
        }

        assert post.has_likes() == expected

    @pytest.mark.parametrize(("liked", "expected"), [
        (1, True),
        (0, False),
    ])
    def test_is_liked(self, vk: FakeVk, post: Post, liked: int, expected: bool) -> None:
        vk.responses = {
            "likes.isLiked": {
                "liked": liked,
            },
        }

        assert post.is_liked(by=1) == expected
        assert vk.params("likes.isLiked").items() >= {
            "type": "post",
            "owner_id": -_GROUP_ID,
            "item_id": 7,
            "user_id": 1,
        }.items()

    def test_like_raises_method_was_deleted(self, vk: FakeVk, post: Post) -> None:
        with pytest.raises(MethodWasDeleted):
            post.like()

        assert vk.calls == []

    def test_object_types(self, vk: FakeVk, post: Post) -> None:
        vk.responses = {
            "wall.getComment": {
                "items": [
                    _COMMENT_OBJECT,
                ],
            },
        }

        comment = post.get_comment(9)
        photo = Photo.from_photo_object(vk, _PHOTO_OBJECT)

        assert (comment.like_object_type, comment.item_id) == ("comment", 9)
        assert (photo.like_object_type, photo.item_id) == ("photo", 3)


class TestEvents:
    def test_get_event(self, vk: FakeVk, pyvko: Pyvko) -> None:
        vk.responses = {
            "groups.getById": {
                "groups": [
                    _EVENT_OBJECT,
                ],
            },
            "groups.getSettings": _SETTINGS_OBJECT,
        }

        event = pyvko.get_event("https://vk.com/event20")

        assert event is not None
        assert event.id == -20
        assert event.name == "Event"
        assert event.end_date == datetime.fromtimestamp(1_700_003_600)
        assert event.event_category == Event.Category.CONCERT
        assert event.main_section == Event.Section.PHOTOS
        assert event.secondary_section == Event.Section.VIDEOS
        assert event.section_state(Event.Section.WALL) == Event.SectionState.ENABLED
        assert event.organiser == -_GROUP_ID
        assert vk.params("groups.getById")["group_id"] == "20"
        assert vk.params("groups.getSettings")["group_id"] == 20

    def test_get_event_without_settings_access(self, vk: FakeVk, pyvko: Pyvko) -> None:
        vk.responses = {
            "groups.getById": {
                "groups": [
                    _EVENT_OBJECT,
                ],
            },
            "groups.getSettings": access_denied,
        }

        event = pyvko.get_event(20)

        assert event is not None
        assert event.event_category is None
        assert event.section_state(Event.Section.WALL) is None

    def test_get_event_returns_none_for_group(self, vk: FakeVk, pyvko: Pyvko) -> None:
        vk.responses = {
            "groups.getById": {
                "groups": [
                    _GROUP_OBJECT,
                ],
            },
        }

        assert pyvko.get_event(_GROUP_ID) is None


class TestUser:
    def test_groups(self, vk: FakeVk) -> None:
        vk.responses = {
            "groups.get": {
                "items": [
                    _GROUP_OBJECT,
                ],
                "count": 1,
            },
        }

        groups = User(vk, _USER_OBJECT).groups()

        assert [group.id for group in groups] == [-_GROUP_ID]
        assert vk.params("groups.get") == {
            "user_id": 1,
            "extended": 1,
        }

    def test_events(self, vk: FakeVk) -> None:
        vk.responses = {
            "groups.get": page(_EVENT_OBJECT),
        }

        events = User(vk, _USER_OBJECT).events()

        assert [event.id for event in events] == [-20]
        assert vk.params("groups.get")["filter"] == "events"

    @pytest.mark.parametrize(("screen_name", "url"), [
        ("ivan", "https://vk.com/ivan"),
        ("", "https://vk.com/id1"),
    ])
    def test_url(self, vk: FakeVk, screen_name: str, url: str) -> None:
        user = User(vk, _USER_OBJECT | {
            "screen_name": screen_name,
        })

        assert user.url == url


class TestPyvko:
    def test_current_user(self, vk: FakeVk, pyvko: Pyvko) -> None:
        vk.responses = {
            "users.get": [
                _USER_OBJECT,
            ],
        }

        user = pyvko.current_user()

        assert (user.id, user.first_name, user.last_name, user.online) == (1, "Ivan", "Ivanov", True)

    def test_get_user(self, vk: FakeVk, pyvko: Pyvko) -> None:
        vk.responses = {
            "users.get": [
                _USER_OBJECT,
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
                "object_id": _GROUP_ID,
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
            group_object = _EVENT_OBJECT if params["group_id"] == "20" else _GROUP_OBJECT

            return {
                "groups": [
                    group_object,
                ],
            }

        vk.responses = {
            "users.get": [
                _USER_OBJECT,
            ],
            "groups.getById": groups_by_id,
            "groups.getSettings": access_denied,
        }

        assert isinstance(pyvko.get(request_), expected_type)

    @pytest.mark.parametrize(("name_type", "groups", "expected_type"), [
        ("user", [_GROUP_OBJECT], User),
        ("group", [_GROUP_OBJECT], Group),
        ("group", [_EVENT_OBJECT], Event),
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
                _USER_OBJECT,
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
