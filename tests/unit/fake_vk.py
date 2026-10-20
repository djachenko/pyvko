from __future__ import annotations

from collections.abc import Callable
from typing import Any

from vk_api.exceptions import ApiError

Response = Any | Callable[[dict[str, Any]], Any]


class FakeMethod:
    def __init__(self, vk: FakeVk, name: str) -> None:
        self.__vk = vk
        self.__name = name

    def __getattr__(self, name: str) -> FakeMethod:
        return FakeMethod(self.__vk, f"{self.__name}.{name}")

    def __call__(self, **params: Any) -> Any:
        return self.__vk.call(self.__name, params)


class FakeVk:
    def __init__(self) -> None:
        self.responses: dict[str, Response] = {}
        self.calls: list[tuple[str, dict[str, Any]]] = []

    def __getattr__(self, name: str) -> FakeMethod:
        return FakeMethod(self, name)

    def call(self, method: str, params: dict[str, Any]) -> Any:
        self.calls.append((method, params))

        response = self.responses[method]

        if callable(response):
            return response(params)

        return response

    def params(self, method: str) -> dict[str, Any]:
        matching = [params for name, params in self.calls if name == method]

        assert len(matching) == 1, f"{method} called {len(matching)} times"

        return matching[0]


def page(*items: Any) -> dict[str, Any]:
    return {
        "items": list(items),
        "count": len(items),
    }


def access_denied(params: dict[str, Any]) -> Any:
    raise ApiError(None, "groups.getSettings", params, False, {
        "error_code": 15,
        "error_msg": "Access denied",
    })
