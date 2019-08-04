import json
from pathlib import Path


class Config:
    def __init__(self, json_object: dict) -> None:
        super().__init__()

        self.__access_token = json_object["token"]

    @classmethod
    def read(cls, path: Path) -> 'Config':
        with path.open() as config:
            json_object = json.load(config)

            return Config(json_object)

    @property
    def access_token(self) -> str:
        return self.__access_token
