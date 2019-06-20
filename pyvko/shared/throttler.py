import time
from typing import Any


class Throttler:

    def __init__(self, obj, interval: float) -> None:
        super().__init__()

        self.__object = obj
        self.__interval = interval
        self.__last_time = time.time() - interval

    def __throttle(self):
        now = time.time()

        sleep_time = self.__interval + self.__last_time - now

        if sleep_time > 0:
            time.sleep(sleep_time)

        self.__last_time = now

    def __getattr__(self, name: str) -> Any:
        self.__throttle()

        return getattr(self.__object, name)
