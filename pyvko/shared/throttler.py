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
        return Throttler(getattr(self.__object, name), self.__interval)

    def __call__(self, *args, **kwargs):
        self.__throttle()

        return self.__object(*args, **kwargs)
