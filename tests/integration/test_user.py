from pyvko.aspects.events import Event
from pyvko.aspects.groups import Group
from pyvko.pyvko_main import Pyvko


def test_user_has_id(pyvko_client: Pyvko):
    user = pyvko_client.current_user()

    assert isinstance(user.id, int)
    assert user.id > 0


def test_user_has_name(pyvko_client: Pyvko):
    user = pyvko_client.current_user()

    assert user.first_name
    assert user.last_name


def test_user_groups(pyvko_client: Pyvko):
    user = pyvko_client.current_user()
    groups = user.groups()

    assert isinstance(groups, list)
    assert all(isinstance(g, Group) for g in groups)


def test_user_events(pyvko_client: Pyvko):
    user = pyvko_client.current_user()
    events = user.events()

    assert isinstance(events, list)
    assert all(isinstance(e, Event) for e in events)
