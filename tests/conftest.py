import os
from pathlib import Path

import pytest

from pyvko.aspects.comments import CommentModel
from pyvko.aspects.posts import PostModel
from pyvko.config.config import Config
from pyvko.pyvko_main import Pyvko


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        pytest.skip(f"{name} env var not set")
    return value


@pytest.fixture(scope="session")
def pyvko_client() -> Pyvko:
    token = _require_env("VK_TOKEN")
    config = Config({"token": token})
    return Pyvko(config)


@pytest.fixture(scope="session")
def test_group(pyvko_client: Pyvko):
    group_url = _require_env("VK_TEST_GROUP")
    group = pyvko_client.get_group(group_url)
    assert group is not None, f"Group not found: {group_url}"
    return group


@pytest.fixture(scope="session")
def created_event(test_group):
    return test_group.create_event("pyvko test event")


@pytest.fixture(scope="session")
def created_post(test_group):
    post = test_group.add_post(PostModel(text="pyvko test"))
    yield post
    test_group.delete_post(post.id)


@pytest.fixture(scope="session")
def created_comment(created_post):
    return created_post.add_comment(CommentModel(text="test comment"))


@pytest.fixture(scope="session")
def created_album(test_group):
    return test_group.create_album("pyvko test album")


@pytest.fixture(scope="session")
def uploaded_photo(created_album):
    photo_path_str = _require_env("VK_TEST_PHOTO")
    photo_path = Path(photo_path_str)
    if not photo_path.exists():
        pytest.skip(f"Test photo not found: {photo_path}")
    return created_album.add_photo(photo_path)


@pytest.fixture(scope="session")
def test_event(pyvko_client: Pyvko):
    event_id = _require_env("VK_TEST_EVENT_ID")
    event = pyvko_client.get_event(int(event_id))
    assert event is not None, f"Event not found: {event_id}"
    return event


@pytest.fixture(scope="session")
def wall_photo(test_group):
    photo_path_str = _require_env("VK_TEST_PHOTO")
    photo_path = Path(photo_path_str)
    if not photo_path.exists():
        pytest.skip(f"Test photo not found: {photo_path}")
    return test_group.upload_photo_to_wall(photo_path)
