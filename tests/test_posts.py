import pytest

from pyvko.aspects.posts import PostModel


@pytest.mark.create
def test_post_created(created_post):
    assert created_post.id is not None
    assert created_post.id > 0


@pytest.mark.create
def test_post_has_text(created_post):
    assert created_post.text == "pyvko test"


@pytest.mark.create
def test_get_post_by_id(test_group, created_post):
    post = test_group.get_post(created_post.id)
    assert post is not None
    assert post.id == created_post.id


@pytest.mark.create
def test_update_post(test_group, created_post):
    created_post.text = "pyvko test (updated)"
    test_group.update_post(created_post)

    refreshed = test_group.get_post(created_post.id)
    assert refreshed.text == "pyvko test (updated)"


@pytest.mark.create
def test_get_posts_list_contains_created(test_group, created_post):
    posts = test_group.get_posts()
    ids = [p.id for p in posts]
    assert created_post.id in ids


@pytest.mark.create
def test_get_scheduled_posts(test_group):
    scheduled = test_group.get_scheduled_posts()
    assert isinstance(scheduled, list)


@pytest.mark.create
def test_wall_photo_uploaded(wall_photo):
    assert isinstance(wall_photo.id, int)
    assert wall_photo.id > 0


@pytest.mark.create
def test_wall_photo_has_url(wall_photo):
    url = wall_photo.largest_link()
    assert url
    assert url.startswith("https://")


@pytest.mark.create
def test_post_with_photo_attachment(test_group, wall_photo):
    post = test_group.add_post(PostModel(text="pyvko test with photo", attachments=[wall_photo]))
    assert post.id > 0
    test_group.delete_post(post.id)
