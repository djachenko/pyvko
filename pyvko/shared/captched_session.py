import webbrowser

from vk import Session


class CaptchedSession(Session):
    def get_captcha_key(self, captcha_image_url: str) -> str:
        while True:
            captcha_key = input(f"Captcha required with url: {captcha_image_url} (press Enter to open in browser): ")

            if captcha_key:
                break
            else:
                webbrowser.open(captcha_image_url)

        return captcha_key
