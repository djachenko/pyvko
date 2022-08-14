from abc import ABC

from pyvko.api_based import ApiMixin


class Utils(ApiMixin, ABC):
    def shorten_link(self, link: str) -> str:
        request = self.get_request({
            "url": link,
            "private": 1,
        })

        response = self.api.utils.getShortLink(**request)

        return response["short_url"]

    def resolve_name(self, url):
        request = self.get_request({
            "screen_name": url
        })

        response = self.api.utils.resolveScreenName(**request)

        t = response["type"]

        return t
