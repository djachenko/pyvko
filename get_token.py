import json
import webbrowser
from pathlib import Path
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


def update_configs(token: str):
    token_object = {
        "token": token,
    }
    str_paths = [
        "C:/Users/justin",
        "C:/Users/justin/projects/justin",
    ]
    root_paths = [Path(path) for path in str_paths]
    config_folders = [path / ".justin" for path in root_paths]
    pyvko_configs = [path / "pyvko_config.json" for path in config_folders]
    for config_path in pyvko_configs:
        with config_path.open("w") as config:
            json.dump(token_object, config, indent=4)


def main():
    token = get_token()
    print(token)
    update_configs(token)


if __name__ == '__main__':
    main()
