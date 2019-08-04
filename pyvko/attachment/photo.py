from pyvko.attachment.attachment import Attachment


class Photo(Attachment):

    def __init__(self, photo_object: dict) -> None:
        super().__init__(
            photo_object["id"],
            photo_object["owner_id"],
            Attachment.Type.PHOTO
        )

    def to_attach(self) -> str:
        return f"photo{self.owner_id}_{self.id}"
