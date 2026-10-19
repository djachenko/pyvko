import pytest


@pytest.mark.create
def test_comment_created(created_comment):
    assert isinstance(created_comment.id, int)
    assert created_comment.id > 0


@pytest.mark.create
def test_comment_has_text(created_comment):
    assert created_comment.text == "test comment"


@pytest.mark.create
def test_get_comment(created_post, created_comment):
    comment = created_post.get_comment(created_comment.id)

    assert comment is not None
    assert comment.id == created_comment.id


@pytest.mark.create
def test_get_comments_list_contains_created(created_post, created_comment):
    comments = created_post.get_comments()
    ids = [c.id for c in comments]

    assert created_comment.id in ids
