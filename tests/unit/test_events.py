from __future__ import annotations

from datetime import datetime

from pyvko.aspects.events import Event
from pyvko.pyvko_main import Pyvko
from tests.unit.fake_vk import FakeVk, access_denied
from tests.unit.vk_objects import EVENT_OBJECT, GROUP_ID, GROUP_OBJECT, SETTINGS_OBJECT


class TestEvents:
    def test_get_event(self, vk: FakeVk, pyvko: Pyvko) -> None:
        vk.responses = {
            "groups.getById": {
                "groups": [
                    EVENT_OBJECT,
                ],
            },
            "groups.getSettings": SETTINGS_OBJECT,
        }

        event = pyvko.get_event("https://vk.com/event20")

        assert event is not None
        assert event.id == -20
        assert event.name == "Event"
        assert event.end_date == datetime.fromtimestamp(1_700_003_600)
        assert event.event_category == Event.Category.CONCERT
        assert event.main_section == Event.Section.PHOTOS
        assert event.secondary_section == Event.Section.VIDEOS
        assert event.section_state(Event.Section.WALL) == Event.SectionState.ENABLED
        assert event.organiser == -GROUP_ID
        assert vk.params("groups.getById")["group_id"] == "20"
        assert vk.params("groups.getSettings")["group_id"] == 20

    def test_get_event_without_settings_access(self, vk: FakeVk, pyvko: Pyvko) -> None:
        vk.responses = {
            "groups.getById": {
                "groups": [
                    EVENT_OBJECT,
                ],
            },
            "groups.getSettings": access_denied,
        }

        event = pyvko.get_event(20)

        assert event is not None
        assert event.event_category is None
        assert event.section_state(Event.Section.WALL) is None

    def test_get_event_returns_none_for_group(self, vk: FakeVk, pyvko: Pyvko) -> None:
        vk.responses = {
            "groups.getById": {
                "groups": [
                    GROUP_OBJECT,
                ],
            },
        }

        assert pyvko.get_event(GROUP_ID) is None
