from functools import lru_cache

from pyvko.attachment.attachment import Attachment
from pyvko.attachment.photo import Photo


class AttachmentParser:
    @staticmethod
    @lru_cache()
    def shared():
        return AttachmentParser()

    def parse_photo(self, api_object: dict) -> Photo:
        return Photo(api_object)

    def parse_object(self, api_object: dict) -> Attachment:
        if "photo" in api_object:
            return self.parse_photo(api_object["photo"])
        else:
            return None
