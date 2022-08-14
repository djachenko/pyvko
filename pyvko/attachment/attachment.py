from abc import abstractmethod


class Attachment:
    @property
    @abstractmethod
    def type(self) -> str:
        pass

    @property
    @abstractmethod
    def owner_id(self) -> int:
        pass

    @property
    @abstractmethod
    def media_id(self) -> int:
        pass

    def to_attach(self) -> str:
        return f"{self.type}{self.owner_id}_{self.media_id}"
