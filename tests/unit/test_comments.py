from __future__ import annotations

from pyvko.aspects.comments import CommentModel
from pyvko.aspects.posts import Post
from tests.unit.fake_vk import FakeVk
from tests.unit.vk_objects import COMMENT_OBJECT, GROUP_ID


class TestComments:
    def test_add_comment(self, vk: FakeVk, post: Post) -> None:
        vk.responses = {
            "wall.createComment": {
                "comment_id": 9,
            },
            "wall.getComment": {
                "items": [
                    COMMENT_OBJECT,
                ],
            },
        }

        comment = post.add_comment(CommentModel(text="comment", from_group=GROUP_ID))

        assert (comment.id, comment.text) == (9, "comment")
        assert vk.params("wall.createComment").items() >= {
            "message": "comment",
            "from_group": GROUP_ID,
            "post_id": 7,
            "owner_id": -GROUP_ID,
        }.items()
        assert vk.params("wall.getComment").items() >= {
            "comment_id": 9,
            "owner_id": -GROUP_ID,
        }.items()

    def test_get_comments(self, vk: FakeVk, post: Post) -> None:
        vk.responses = {
            "wall.getComments": {
                "items": [
                    COMMENT_OBJECT,
                ],
                "count": 5,
                "current_level_count": 1,
            },
        }

        comments = post.get_comments()

        assert [comment.id for comment in comments] == [9]
        assert vk.params("wall.getComments").items() >= {
            "post_id": 7,
            "owner_id": -GROUP_ID,
            "offset": 0,
        }.items()
