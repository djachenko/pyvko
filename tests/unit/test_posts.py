from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest
import requests

from pyvko.aspects.albums import Album
from pyvko.aspects.groups import Group
from pyvko.aspects.posts import Post, PostModel
from pyvko.attachment.attachment_parser import Link
from pyvko.attachment.photo import Photo
from tests.unit.fake_vk import FakeVk, page
from tests.unit.vk_objects import ALBUM_OBJECT, GROUP_ID, PHOTO_OBJECT, POST_OBJECT


class TestPosts:
    def test_get_posts(self, vk: FakeVk, group: Group) -> None:
        vk.responses = {
            "wall.get": page(POST_OBJECT),
        }

        posts = group.get_posts()

        assert [(post.id, post.text, post.owner_id) for post in posts] == [(7, "post", -GROUP_ID)]
        assert vk.params("wall.get") == {
            "count": 100,
            "owner_id": -GROUP_ID,
            "offset": 0,
        }

    def test_get_posts_by_ids_skips_deleted(self, vk: FakeVk, group: Group) -> None:
        deleted = POST_OBJECT | {
            "id": 8,
            "is_deleted": True,
        }
        vk.responses = {
            "wall.getById": {
                "items": [
                    POST_OBJECT,
                    deleted,
                ],
            },
        }

        posts = group.get_posts(7, 8)

        assert [post.id for post in posts] == [7]
        assert vk.params("wall.getById") == {
            "posts": [
                f"-{GROUP_ID}_7",
                f"-{GROUP_ID}_8",
            ],
        }

    @pytest.mark.parametrize(("items", "expected_id"), [
        ([POST_OBJECT], 7),
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
            "wall.get": page(POST_OBJECT | {
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
                    POST_OBJECT,
                ],
            },
        }
        model = PostModel(
            text="post",
            attachments=[Album(vk, ALBUM_OBJECT)],
            date=datetime.fromtimestamp(1_800_000_000),
        )

        post = group.add_post(model)

        assert post.id == 7
        assert vk.params("wall.post") == {
            "from_group": 1,
            "primary_attachments_mode": "grid",
            "message": "post",
            "attachments": f"album-{GROUP_ID}_5",
            "publish_date": 1_800_000_000,
            "owner_id": -GROUP_ID,
        }

    def test_update_post(self, vk: FakeVk, group: Group, post: Post) -> None:
        vk.responses = {
            "wall.edit": 1,
        }
        post.text = "edited"

        group.update_post(post)

        params = vk.params("wall.edit")

        assert params["post_id"] == 7
        assert params["owner_id"] == -GROUP_ID
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
                PHOTO_OBJECT,
            ],
        }

        photo = group.upload_photo_to_wall(photo_path)

        assert photo.id == 3
        assert sent_urls == ["https://upload.example/wall"]
        assert vk.params("photos.getWallUploadServer") == {
            "group_id": GROUP_ID,
        }
        assert vk.params("photos.saveWallPhoto") == {
            "group_id": GROUP_ID,
        } | upload_response

    def test_parses_attachments(self, vk: FakeVk) -> None:
        post_object = POST_OBJECT | {
            "attachments": [
                {
                    "photo": PHOTO_OBJECT,
                },
                {
                    "album": ALBUM_OBJECT,
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
