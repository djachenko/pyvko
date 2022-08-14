from dataclasses import dataclass
from datetime import datetime
from typing import List

from pyvko.attachment.attachment import Attachment


@dataclass
class PostModel:
    text: str = None
    attachments: List[Attachment] = None
    date: datetime = None

    def to_request(self) -> dict:
        request = {}

        if self.text is not None:
            request["message"] = self.text

        if self.attachments is not None:
            request["attachments"] = ",".join([a.to_attach() for a in self.attachments])

        if self.date is not None:
            request["publish_date"] = self.date.timestamp()

        return request

