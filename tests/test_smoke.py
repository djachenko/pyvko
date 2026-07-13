import pytest

from pyvko.aspects.groups import Group
from pyvko.pyvko_main import Pyvko


@pytest.mark.smoke
def test_auth_current_user(pyvko_client: Pyvko):
    user = pyvko_client.current_user()
    assert user.id > 0


@pytest.mark.smoke
def test_resolve_group_name(pyvko_client: Pyvko, test_group):
    result = pyvko_client.resolve_name(test_group.url)

    assert result == "group"


@pytest.mark.smoke
def test_get_by_url_returns_group(pyvko_client: Pyvko, test_group):
    result = pyvko_client.get_by_url(test_group.url)
    assert isinstance(result, Group)


@pytest.mark.smoke
def test_shorten_link(pyvko_client: Pyvko):
    short = pyvko_client.shorten_link("https://vk.com")
    assert isinstance(short, str)
    assert short.startswith("https://vk.cc")
