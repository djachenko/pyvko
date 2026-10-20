from __future__ import annotations

import pytest

from pyvko.api_based import ApiBased
from pyvko.aspects.groups import Group
from pyvko.aspects.posts import Post
from pyvko.pyvko_main import Pyvko
from tests.unit.fake_vk import FakeVk
from tests.unit.vk_objects import GROUP_OBJECT, POST_OBJECT


@pytest.fixture
def vk() -> FakeVk:
    return FakeVk()


@pytest.fixture
def group(vk: FakeVk) -> Group:
    return Group(api=vk, group_object=GROUP_OBJECT)


@pytest.fixture
def post(vk: FakeVk) -> Post:
    return Post.from_post_object(POST_OBJECT, vk)


@pytest.fixture
def pyvko(vk: FakeVk) -> Pyvko:
    client = Pyvko.__new__(Pyvko)

    ApiBased.__init__(client, vk)

    return client
