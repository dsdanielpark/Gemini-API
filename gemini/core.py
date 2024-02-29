import requests
import re
import random
import string
import json
import urllib.parse
from .constants import HEADERS, HOST, BOT_SERVER, POST_ENDPOINT


class Gemini:
    def __init__(self, cookies=None):
        self.session = requests.Session()
        self.base_url = HOST
        self.session.headers.update(HEADERS)
        if cookies:
            self.session.cookies.update(cookies)

    def _get_sid_and_nonce(self):
        try:
            response = self.session.get(f"{self.base_url}/app")
            response.raise_for_status()
        except requests.RequestException as e:
            raise ConnectionError(f"Failed to connect to {self.base_url}: {e}")

        sid = self._search_regex(response.text, r'"FdrFJe":"([\d-]+)"', "SID")
        nonce = self._search_regex(response.text, r'"SNlM0e":"(.*?)"', "nonce")

        return sid, nonce

    @staticmethod
    def _search_regex(text, pattern, term):
        match = re.search(pattern, text)
        if not match:
            raise ValueError(f"Failed to extract {term}.")
        return match.group(1)

    @staticmethod
    def _get_reqid():
        return int("".join(random.choices(string.digits, k=7)))

    def _construct_params(self, sid):
        return urllib.parse.urlencode(
            {
                "bl": BOT_SERVER,
                "hl": "en",
                "_reqid": self._get_reqid(),
                "rt": "c",
                "f.sid": sid,
            }
        )

    def _construct_payload(self, prompt, nonce):
        return urllib.parse.urlencode(
            {
                "at": nonce,
                "f.req": json.dumps([None, json.dumps([[prompt], None, None])]),
            }
        )

    def send_request(self, prompt):
        try:
            sid, nonce = self._get_sid_and_nonce()
        except Exception as e:
            return f"Error retrieving session data: {e}", None

        params = self._construct_params(sid)
        data = self._construct_payload(prompt, nonce)

        try:
            response = self.session.post(
                POST_ENDPOINT,
                params=params,
                data=data,
            )
            response.raise_for_status()
        except requests.RequestException as e:
            return f"Request failed: {e}", None

        return response.text, response.status_code
