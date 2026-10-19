import pytest

from pyvko.aspects.events import Event
from pyvko.pyvko_main import Pyvko


@pytest.mark.create
class TestCreatedEvent:
    def test_has_id(self, created_event):
        assert isinstance(created_event.id, int)
        assert created_event.id != 0

    def test_has_name(self, created_event):
        assert created_event.name == "pyvko test event"

    def test_has_start_date(self, created_event):
        assert created_event.start_date is not None

    def test_section_state_wall(self, created_event):
        state = created_event.section_state(Event.Section.WALL)

        # None when event settings are not accessible (no admin rights or API error 15)
        if state is not None:
            assert isinstance(state, Event.SectionState)

    def test_set_section_state(self, created_event):
        current = created_event.section_state(Event.Section.PHOTOS)

        if current is None or current == Event.SectionState.NOT_AVAILABLE:
            pytest.skip("PHOTOS section not accessible on this event")

        if current == Event.SectionState.DISABLED:
            new_state = Event.SectionState.OPEN
        else:
            new_state = Event.SectionState.DISABLED

        created_event.set_section_state(Event.Section.PHOTOS, new_state)
        created_event.save()

    def test_get_by_id(self, pyvko_client: Pyvko, created_event):
        event = pyvko_client.get_event(abs(created_event.id))

        assert event is not None
        assert event.id == created_event.id


class TestExistingEvent:
    def test_has_id(self, test_event):
        assert isinstance(test_event.id, int)
        assert test_event.id != 0

    def test_has_name(self, test_event):
        assert isinstance(test_event.name, str)
        assert test_event.name

    def test_has_start_date(self, test_event):
        assert test_event.start_date is not None

    def test_get_posts(self, test_event):
        posts = test_event.get_posts()

        assert isinstance(posts, list)
