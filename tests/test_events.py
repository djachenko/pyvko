import pytest

from pyvko.aspects.events import Event
from pyvko.pyvko_main import Pyvko


@pytest.mark.create
def test_event_created(created_event):
    assert isinstance(created_event.id, int)
    assert created_event.id != 0


@pytest.mark.create
def test_event_has_name(created_event):
    assert created_event.name == "pyvko test event"


@pytest.mark.create
def test_event_has_start_date(created_event):
    assert created_event.start_date is not None


@pytest.mark.create
def test_event_section_state_wall(created_event):
    state = created_event.section_state(Event.Section.WALL)
    # None when event settings are not accessible (no admin rights or API error 15)
    if state is not None:
        assert isinstance(state, Event.SectionState)


@pytest.mark.create
def test_event_set_section_state(created_event):
    current = created_event.section_state(Event.Section.PHOTOS)
    if current is None or current == Event.SectionState.NOT_AVAILABLE:
        pytest.skip("PHOTOS section not accessible on this event")

    new_state = (
        Event.SectionState.OPEN
        if current == Event.SectionState.DISABLED
        else Event.SectionState.DISABLED
    )
    created_event.set_section_state(Event.Section.PHOTOS, new_state)
    created_event.save()


@pytest.mark.create
def test_get_event_by_id(pyvko_client: Pyvko, created_event):
    event = pyvko_client.get_event(abs(created_event.id))
    assert event is not None
    assert event.id == created_event.id
