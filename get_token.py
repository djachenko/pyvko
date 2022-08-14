import json
import webbrowser
from pathlib import Path
from urllib.parse import urlencode, parse_qs


def get_token() -> str:
    params = {
        "client_id": 5503908,
        "scope": ",".join([
            # "notify",         # (+1)      	User allowed to send notifications to him/her (for Flash/iFrame apps).
            # "friends",        # (+2)      	Access to friends.
            "photos",           # (+4)      	Access to photos.
            # "audio",          # (+8)      	Access to audio.
            # "video",          # (+16)     	Access to video.
            # "stories",        # (+64)     	Access to stories.
            # "pages",          # (+128)        Access to wiki pages.
            # "no value"        # (+256)        Addition of link to the application in the left menu.
            # "status",         # (+1024)       Access to user status.
            # "notes",          # (+2048)       Access to notes.
            "messages",         # (+4096)       (for Standalone applications) Access to advanced methods for messaging.
            "wall",             # (+8192)       Access to standard and advanced methods for the wall. Note that this access permission is unavailable for sites (it is ignored at attempt of authorization).
            # "ads",            # (+32768)      Access to advanced methods for Ads API.
            "offline",          # (+65536)      Access to API at any time (you will receive expires_in = 0 in this case).
            "docs",             # (+131072)     Access to docs.
            "groups",           # (+262144)     Access to user communities.
            # "notifications",  # (+524288)     Access to notifications about answers to the user.
            # "stats",          # (+1048576)    Access to statistics of user groups and applications where he/she is an administrator.
            # "email",          # (+4194304)    Access to user email.
            # "market",         # (+134217728)  Access to market.
        ]),
        "redirect_uri": "http://oauth.vk.com/blank.html",
        "display": "page",
        "response_type": "token",
        "v": 5.131
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
