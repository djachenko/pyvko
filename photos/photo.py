from attachment import Attachment


class Photo(Attachment):

    def __init__(self, photo_object: dict) -> None:
        super().__init__(
            photo_object["id"],
            photo_object["owner_id"],
            Attachment.Type.PHOTO
        )
