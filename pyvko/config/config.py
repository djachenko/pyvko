import json
from pathlib import Path


class Config:
    def __init__(self, path_to_config_file: Path) -> None:
        super().__init__()

        with path_to_config_file.open() as config:
            data = json.load(config)

            self.__access_token = data["token"]

    @property
    def access_token(self) -> str:
        return self.__access_token
