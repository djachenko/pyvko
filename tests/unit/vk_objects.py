from pyvko.aspects.events import Event

GROUP_ID = 10

GROUP_OBJECT = {
    "id": GROUP_ID,
    "name": "Group",
    "screen_name": "group",
    "type": "group",
}

USER_OBJECT = {
    "id": 1,
    "first_name": "Ivan",
    "last_name": "Ivanov",
    "online": 1,
    "screen_name": "ivan",
}

PHOTO_OBJECT = {
    "id": 3,
    "owner_id": -GROUP_ID,
    "sizes": [
        {
            "type": "x",
            "url": "https://photo/x",
        },
    ],
    "text": "photo",
}

ALBUM_OBJECT = {
    "id": 5,
    "owner_id": -GROUP_ID,
    "title": "Album",
}

POST_OBJECT = {
    "id": 7,
    "owner_id": -GROUP_ID,
    "text": "post",
    "date": 1_700_000_000,
}

COMMENT_OBJECT = {
    "id": 9,
    "owner_id": -GROUP_ID,
    "text": "comment",
    "date": 1_700_000_000,
}

EVENT_OBJECT = {
    "id": 20,
    "name": "Event",
    "screen_name": "event20",
    "type": "event",
    "start_date": 1_700_000_000,
    "finish_date": 1_700_003_600,
    "is_closed": 0,
}

SETTINGS_OBJECT = {
    "public_category": Event.Category.CONCERT.value,
    "main_section": 1,
    "secondary_section": 4,
    "event_object_id": -GROUP_ID,
} | {section.value: Event.SectionState.ENABLED.value for section in Event.Section}
