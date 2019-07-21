from abc import abstractmethod
from enum import Enum, auto


class Attachment:
    class Type(Enum):
        PHOTO = auto()

    def __init__(self, self_id: int, owner_id: int, attach_type) -> None:
        super().__init__()

        self.type: Attachment.Type = attach_type
        self.id = self_id
        self.owner_id = owner_id

    @abstractmethod
    def to_attach(self) -> str:
        return f"photo{self.owner_id}_{self.id}"
