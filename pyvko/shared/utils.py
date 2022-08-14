import time
import webbrowser
from typing import Generator, Dict, Callable, Union, List, Any

from vk import Session


def get_all(parameters: Dict, get_response: Callable[[], Dict[str, Union[int, List[Dict]]]]) \
        -> Generator[Dict, None, None]:
    parameters = parameters.copy()
    total = 0

    while True:
        parameters["offset"] = total

        # noinspection PyArgumentList
        response = get_response(**parameters)

        assert "items" in response
        assert "count" in response

        descriptions_chunk = response["items"]
        count = response["count"]

        total += len(descriptions_chunk)

        for desc in descriptions_chunk:
            yield desc

        if count == total:
            break


class CaptchedSession(Session):
    def get_captcha_key(self, captcha_image_url: str) -> str:
        while True:
            captcha_key = input(f"Captcha required with url: {captcha_image_url} (press Enter to open in browser): ")

            if captcha_key:
                break
            else:
                webbrowser.open(captcha_image_url)

        return captcha_key


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
