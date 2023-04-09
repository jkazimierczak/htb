from requests import Session


LOGIN_URL = f"https://panel.ct8.pl/login/"


def prepare_header(csrf_token):
    return {
        "Host": "panel.ct8.pl",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 HTB/111.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/x-www-form-urlencoded",
        # "Content-Length": "145",
        "Origin": "https://panel.ct8.pl",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": "https://panel.ct8.pl/login/",
        "Cookie": f"csrftoken={csrf_token}",
        "Upgrade-Insecure-Requests": "1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }


class CT8:
    def __init__(self):
        self.session = Session()

    def login(self, username: str, password: str):
        """Login to CT8 panel with supplied credentials."""

        self.session.get(LOGIN_URL)
        csrf_token = self.session.cookies.get("csrftoken")

        headers = prepare_header(csrf_token)
        login_data = {
            "csrfmiddlewaretoken": csrf_token,
            "username": username,
            "password": password,
        }

        # Sign-in
        res = self.session.post(
            LOGIN_URL, data=login_data, headers=headers, allow_redirects=False
        )

        if res.status_code == 302:
            if res.next:
                self.session.send(res.next)
            print(f"Login successful - {username}.")
        else:
            print(f"Login failed for {username}.")
