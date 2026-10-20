from __future__ import annotations

import pytest

from pyvko.aspects.likes import Like
from pyvko.aspects.posts import Post
from pyvko.attachment.photo import Photo
from pyvko.shared.exceptions import MethodWasDeleted
from tests.unit.fake_vk import FakeVk, page
from tests.unit.vk_objects import COMMENT_OBJECT, GROUP_ID, PHOTO_OBJECT


class TestLikes:
    def test_get_likes(self, vk: FakeVk, post: Post) -> None:
        vk.responses = {
            "likes.getList": page(1, 2),
        }

        assert post.get_likes() == [Like(author_id=1), Like(author_id=2)]
        assert vk.params("likes.getList").items() >= {
            "type": "post",
            "owner_id": -GROUP_ID,
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
            "owner_id": -GROUP_ID,
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
                    COMMENT_OBJECT,
                ],
            },
        }

        comment = post.get_comment(9)
        photo = Photo.from_photo_object(vk, PHOTO_OBJECT)

        assert (comment.like_object_type, comment.item_id) == ("comment", 9)
        assert (photo.like_object_type, photo.item_id) == ("photo", 3)
