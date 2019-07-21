import webbrowser
from urllib.parse import urlencode, parse_qs


def get_token() -> str:
    params = {
        "client_id": 5503908,
        "scope": ",".join([
            "messages",
            "wall",
            "groups",
            "photos",
            "offline",
            "docs"
        ]),
        "redirect_uri": "http://oauth.vk.com/blank.html",
        "display": "page",
        "response_type": "token",
        "v": 5.92
    }

    params = urlencode(params)

    auth_url = "https://oauth.vk.com/authorize?" + params

    webbrowser.open_new_tab(auth_url)

    redirected_url = input("Paste here url you were redirected:\n")
    redirected_url.strip(" ")

    arguments = parse_qs(redirected_url)

    arguments['access_token'] = arguments.pop(
        'https://oauth.vk.com/blank.html#access_token')

    arguments = {key: [i.strip() for i in value] for key, value in arguments.items()}

    return arguments['access_token'][0]


if __name__ == '__main__':
    token = get_token()

    a = 7
