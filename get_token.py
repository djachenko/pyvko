import webbrowser
from urllib.parse import urlencode, parse_qs


def get_token() -> str:
    params = {
        "client_id": 5503908,
        "scope": ",".join([
            "notify",         # (+1)           User allowed to send notifications to him/her.
            "friends",        # (+2)           Access to friends.
            "photos",         # (+4)           Access to photos.
            "audio",          # (+8)           Access to audio.
            "video",          # (+16)          Access to video.
            "stories",        # (+64)          Access to stories.
            "pages",          # (+128)         Access to wiki pages.
            "status",         # (+1024)        Access to user status.
            "notes",          # (+2048)        Access to notes.
            "messages",       # (+4096)        Access to advanced messaging methods (Standalone only).
            "wall",           # (+8192)        Access to wall methods.
            "ads",            # (+32768)       Access to Ads API.
            "offline",        # (+65536)       Access to API at any time (expires_in = 0).
            "docs",           # (+131072)      Access to docs.
            "groups",         # (+262144)      Access to user communities.
            "notifications",  # (+524288)      Access to notifications about answers.
            "stats",          # (+1048576)     Access to statistics of groups and apps.
            "email",          # (+4194304)     Access to user email.
            "market",         # (+134217728)   Access to market.
        ]),
        "redirect_uri": "https://oauth.vk.com/blank.html",
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


def main():
    token = get_token()
    print(token)


if __name__ == '__main__':
    main()
