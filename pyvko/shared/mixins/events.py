from abc import ABC

from pyvko.api_based import ApiMixin
from pyvko.entities.event import Event


class Events(ApiMixin, ABC):
    # noinspection PyUnresolvedReferences
    def create_event(self, title: str) -> 'Event':
        request = self.get_request({
            "title": title,
            "type": "event",
        })

        response = self.api.groups.create(**request)

        event = self.get_event(response["id"])

        return event

    def get_event(self, url: str) -> Event | None:
        # if not url.isdecimal():
        #     prefix = "event"
        #     parse_result = urlparse(url)
        #
        #     url: str = parse_result.path.split("/")[-1]
        #
        #     if not url.startswith(prefix):
        #         return None
        #
        #     url = url.removeprefix(prefix)
        #
        # if not url.isdecimal():
        #     return None

        group_request = self.get_request({
            "group_id": url,
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

        event_object = event_response[0]

        if event_object["type"] not in ["event", ]:
            return None

        group_request["group_id"] = event_object["id"]

        settings_response = self.api.groups.getSettings(**group_request)

        event = Event(self.api, event_object=event_object, settings_object=settings_response)

        return event
