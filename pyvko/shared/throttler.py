import time
from typing import Any


class Throttler:
    class Context:
        def __init__(self, initial_offset: float) -> None:
            super().__init__()

            self.__time = time.time() - initial_offset

        @property
        def time(self) -> float:
            return self.__time

        @time.setter
        def time(self, value: float):
            self.__time = value

    def __init__(self, obj, interval: float, context: Context = None) -> None:
        super().__init__()

        if context is None:
            context = Throttler.Context(interval)

        self.__object = obj
        self.__interval = interval
        self.__context = context

    def __throttle(self):
        now = time.time()

        sleep_time = self.__context.time + self.__interval - now

        if sleep_time > 0:
            time.sleep(sleep_time)

        self.__context.time = now

    def __getattr__(self, name: str) -> Any:
        return Throttler(getattr(self.__object, name), self.__interval, self.__context)

    def __call__(self, *args, **kwargs):
        self.__throttle()

        return self.__object(*args, **kwargs)
