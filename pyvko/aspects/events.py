from abc import ABC
from datetime import datetime
from enum import Enum
from functools import lru_cache
from typing import Optional, List, Dict, Tuple
from urllib.parse import urlparse

from vk import API
from vk.exceptions import VkAPIError, ErrorCodes

from pyvko.api_based import ApiMixin, ApiBased
from pyvko.aspects.albums import Albums
from pyvko.aspects.posts import Posts


class Event(ApiBased, Posts, Albums):
    class Category(Enum):
        CIRCUS = 1120
        CONCERT = 1107
        PARTY = 1103
        EXHIBITION = 1104

    class Section(Enum):
        WALL = "wall"
        DISCUSSION = "topics"
        PHOTOS = "photos"
        VIDEOS = "video"
        MUSIC = "audio"
        FILES = "docs"
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

    def __init__(self, api: API, event_object: Dict, settings_object: Dict | None) -> None:
        super().__init__(api)

        self.__id: int = -event_object["id"]
        self.name = event_object["name"]
        self.start_date: datetime = datetime.fromtimestamp(event_object["start_date"])
        self.end_date: datetime | None

        if "finish_date" in event_object:
            self.end_date = datetime.fromtimestamp(event_object["finish_date"])
        else:
            self.end_date = None

        self.is_closed = bool(event_object["is_closed"])
        self.url = event_object["screen_name"]

        self.event_category: Event.Category | None

        if settings_object is None:
            self.event_category = None
            self.__sections: Dict[Event.Section, Event.SectionState] = {}
            self.main_section = None
            self.secondary_section = None
            self.organiser = None
        else:
            category_value = settings_object["public_category"]

            if category_value != 0:
                self.event_category = Event.Category(category_value)
            else:
                self.event_category = None

            self.__sections: Dict[Event.Section, Event.SectionState] = {
                s: Event.SectionState(settings_object[s.value]) for s in Event.Section
            }

            self.main_section = Event.Section.from_index(settings_object["main_section"])
            self.secondary_section = Event.Section.from_index(settings_object["secondary_section"])
            self.organiser: int | None = settings_object.get("event_object_id")

    @property
    def id(self) -> int:
        return self.__id

    @property
    def browser_url(self):
        return f"http://vk.com/event{abs(self.id)}"

    def section_state(self, section: Section) -> Optional[SectionState]:
        return self.__sections.get(section)

    def set_section_state(self, section: Section, new_state: SectionState):
        assert new_state != Event.SectionState.NOT_AVAILABLE
        assert self.__sections[section] != Event.SectionState.NOT_AVAILABLE

        self.__sections[section] = new_state

    def save(self):
        params = {
            "group_id": abs(self.__id),
            "access": int(self.is_closed),
            "event_start_date": int(self.start_date.timestamp()),
            "title": self.name,
        }

        for section, state in self.__sections.items():
            if state == Event.SectionState.NOT_AVAILABLE:
                continue

            params[section.value] = state.value

        if self.end_date is not None:
            params["event_finish_date"] = int(self.end_date.timestamp())

        if self.event_category is not None:
            params["public_category"] = self.event_category.value

        if self.main_section is not None:
            params["main_section"] = self.main_section.to_index()

        if self.secondary_section is not None:
            params["secondary_section"] = self.secondary_section.to_index()

        if self.organiser is not None:
            params["event_group_id"] = abs(self.organiser)

        request = self.get_request(params)

        self.api.groups.edit(**request)


class Events(ApiMixin, ABC):
    def create_event(self, title: str) -> Event:
        request = self.get_request({
            "title": title,
            "type": "event",
        })

        response = self.api.groups.create(**request)

        event = self.get_event(response["id"])

        return event

    def get_event(self, url: str | int) -> Event | None:
        url = str(url)

        parse_result = urlparse(url)

        qualifier = parse_result.path \
            .split("/")[-1] \
            .removeprefix("event") \
            .removeprefix("-")

        group_request = self.get_request({
            "group_id": qualifier,
            "fields": [
                "start_date",
                "finish_date",
            ]
        })

        event_request = {
            "fields": [
                "start_date",
                "finish_date",
                "main_section",
            ]
        }

        event_request.update(group_request)

        event_response = self.api.groups.getById(**event_request)

        event_object = event_response["groups"][0]

        if event_object["type"] not in ["event", ]:
            return None

        group_request["group_id"] = event_object["id"]

        try:
            settings_response = self.api.groups.getSettings(**group_request)
        except VkAPIError as err:
            if err.code != ErrorCodes.ACCESS_DENIED:
                raise

            settings_response = None

        event = Event(self.api, event_object=event_object, settings_object=settings_response)

        return event
