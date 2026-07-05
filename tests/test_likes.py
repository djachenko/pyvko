import pytest

from pyvko.aspects.likes import Like


@pytest.mark.create
def test_like_post(created_post):
    created_post.like()


@pytest.mark.create
def test_is_liked_after_like(created_post):
    assert created_post.is_liked()


@pytest.mark.create
def test_get_likes_not_empty(created_post):
    likes = created_post.get_likes()
    assert isinstance(likes, list)
    assert len(likes) > 0
    assert all(isinstance(like, Like) for like in likes)


@pytest.mark.create
def test_has_likes_true(created_post):
    assert created_post.has_likes()
