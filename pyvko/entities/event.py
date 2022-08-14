from datetime import datetime
from enum import Enum
from functools import lru_cache
from typing import Optional, List, Tuple, Dict

from vk import API

from pyvko.api_based import ApiBased
from pyvko.shared.mixins.albums import Albums
from pyvko.shared.mixins.wall import Wall


class Event(ApiBased, Wall, Albums):
    class Category(Enum):
        CIRCUS = 1120

    class Section(Enum):
        PHOTOS = "photos"
        WALL = "wall"
        VIDEOS = "video"
        MUSIC = "audio"
        FILES = "docs"
        DISCUSSION = "topics"
        WIKI = "wiki"
        ARTICLES = "articles"
        NARRATIVES = "narratives"
        MESSAGES = "messages"

        @staticmethod
        @lru_cache()
        def __section_index_mapping() -> List[Tuple['Event.Section', int]]:
            return [
                (Event.Section.PHOTOS, 1),
                (Event.Section.VIDEOS, 4),
            ]

        @classmethod
        def from_index(cls, index: int) -> Optional['Event.Section']:

            for section, section_index in Event.Section.__section_index_mapping():
                if index == section_index:
                    return section

            return None

        def to_index(self) -> Optional[int]:
            for section, section_index in Event.Section.__section_index_mapping():
                if section == self:
                    return section_index

            return None

    class SectionState(Enum):
        NOT_AVAILABLE = -1
        DISABLED = 0
        OPEN = 1
        ENABLED = 1
        LIMITED = 2
        RESTRICTED = 3

    def __init__(self, api: API, event_object: Dict, settings_object: Dict) -> None:
        super().__init__(api)

        self.__id: int = -event_object["id"]
        self.name = event_object["name"]
        self.start_date: datetime = datetime.fromtimestamp(event_object["start_date"])
        self.end_date: datetime | None

        if "finish_date" in event_object:
            self.end_date = datetime.fromtimestamp(event_object["finish_date"])
        else:
            self.end_date = None

        category_value = settings_object["public_category"]
        self.event_category: Optional[Event.Category]

        if category_value != 0:
            self.event_category = Event.Category(category_value)
        else:
            self.event_category = None

        self.__sections: Dict[Event.Section, Event.SectionState] = {
            s: Event.SectionState(settings_object[s.value]) for s in Event.Section
        }

        self.main_section = Event.Section.from_index(settings_object["main_section"])
        self.secondary_section = Event.Section.from_index(settings_object["secondary_section"])
        self.is_closed = bool(event_object["is_closed"])
        self.organiser: int | None = settings_object.get("event_object_id")

    @property
    def id(self) -> int:
        return self.__id

    def section_state(self, section: Section) -> Optional[SectionState]:
        return self.__sections.get(section)

    def set_section_state(self, section: Section, new_state: SectionState):
        assert new_state != Event.SectionState.NOT_AVAILABLE
        assert self.__sections[section] != Event.SectionState.NOT_AVAILABLE

        self.__sections[section] = new_state

    def save(self):
        params = {
            "group_id": self.__id,
            "access": int(self.is_closed),
            "event_start_date": self.start_date.timestamp(),
            "title": self.name,
        }

        for section, state in self.__sections.items():
            if state == Event.SectionState.NOT_AVAILABLE:
                continue

            params[section.value] = state.value

        if self.end_date is not None:
            params["event_finish_date"] = self.end_date.timestamp()

        if self.event_category is not None:
            params["public_category"] = self.event_category.value

        if self.main_section is not None:
            params["main_section"] = self.main_section.to_index()

        if self.secondary_section is not None:
            params["secondary_section"] = self.secondary_section.to_index()

        if self.organiser is not None:
            params["event_group_id"] = self.organiser

        request = self.get_request(params)

        self.api.groups.edit(**request)
