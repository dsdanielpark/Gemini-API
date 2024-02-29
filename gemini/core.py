# Copyright 2024 Daniel Park, Antonio Cheang, MIT License

import os
import re
import json
import random
import string
import requests
import urllib.parse
from typing import Optional, Tuple, Dict, Any
from requests.exceptions import RequestException

from .constants import HEADERS, HOST, BOT_SERVER, POST_ENDPOINT, SUPPORTED_BROWSERS


class Gemini:
    def __init__(
        self,
        session: Optional[requests.Session] = None,
        cookies: Optional[Dict[str, str]] = None,
        cookie_fp: str = None,
        auto_cookies: bool = False,
        timeout: int = 30,
        proxies: Optional[dict] = None,
    ) -> None:
        self.auto_cookies = auto_cookies
        self.cookies = cookies or {}
        self._set_cookies(auto_cookies)
        self.proxies = proxies or {}
        self.timeout = timeout
        self.session = self._set_session(session)
        self.session: requests.Session = requests.Session()
        self.base_url: str = HOST

        self.session.headers.update(HEADERS)
        if cookies:
            self.session.cookies.update(cookies)

        if cookie_fp:
            self._load_cookies_from_file(cookie_fp)

    def _set_cookies(self, auto_cookies: bool) -> None:
        """
        Updates the instance's cookies attribute with Gemini API tokens, either from environment variables or by extracting them from the browser, based on the auto_cookies flag.

        Args:
            auto_cookies (bool): Indicates whether to attempt automatic extraction of tokens from the browser's cookies.

        Raises:
            Exception: If no cookies are provided through environment variables or cannot be extracted from the browser when auto_cookies is True.
        """
        if auto_cookies and not self.cookies:
            try:
                self._set_cookies_from_browser()  # Assuming this updates self.cookies directly
            except Exception as e:
                raise Exception("Failed to extract cookies from browser.") from e
        if not auto_cookies and not self.cookies:
            print(
                "Cookie loading issue, try setting auto_cookies to True. Restart browser, log out, log in for Gemini Web UI to work. Keep a single browser open."
            )
        if not self.cookies:
            raise Exception(
                "Gemini cookies must be provided through environment variables or extracted from the browser with auto_cookies enabled."
            )

    def _set_cookies_from_browser(self) -> None:
        """
        Extracts Gemini cookies from web browsers' cookies on the system for a specific domain (".google.com").

        Iterates over supported browsers to add found cookies to the instance's cookie store. Supports multiple browsers and OS.

        Updates `cookies` attribute with found cookies.

        Raises:
            ValueError: If essential cookies are missing after checking all supported browsers.
        """
        for browser_fn in SUPPORTED_BROWSERS:
            try:
                print(f"Retrieving cookies from {browser_fn} via browser_cookie3.")
                cj = browser_fn(domain_name=".google.com")
                self.cookies.update({cookie.name: cookie.value for cookie in cj})
            except Exception:
                continue  # Try the next browser if an exception occurs

        if not self.cookies:
            raise ValueError(
                "Failed to get cookies. Ensure 'auto_cookies' is True or manually set 'cookies'."
            )

    def check_session_cookies(self) -> None:
        """
        Prints the session's cookies. Indicates if the session is uninitialized.
        """
        if self.session:
            cookies = self.session.cookies.get_dict()
            cookies_str = "\n".join(f"{key}: {value}" for key, value in cookies.items())
            print(f"Session Cookies:\n{cookies_str}")
        else:
            print("Session not initialized.")

    def check_session_headers(self) -> None:
        """
        Prints the session's headers. Indicates if the session is uninitialized.
        """
        if self.session:
            headers = self.session.headers
            headers_str = "\n".join(f"{key}: {value}" for key, value in headers.items())
            print(f"Session Headers:\n{headers_str}")
        else:
            print("Session not initialized.")

    def _load_cookies_from_file(self, file_path: str) -> None:
        """Loads cookies from a file and updates the session."""
        try:
            if file_path.endswith(".json"):
                with open(file_path, "r") as file:
                    cookies = json.load(file)
            else:  # Assuming txt or other formats
                with open(file_path, "r") as file:
                    content = file.read()
                    # Evaluating the dictionary-like string
                    try:
                        cookies = eval(content)
                    except NameError:
                        # Fallback if eval fails due to undefined names
                        cookies = json.loads(content.replace("'", '"'))
            self.session.cookies.update(cookies)
        except Exception as e:
            print(f"Error loading cookie file: {e}")

    def _get_sid_and_nonce(self) -> Tuple[str, str]:
        try:
            response: requests.Response = self.session.get(f"{self.base_url}/app")
            response.raise_for_status()
        except RequestException as e:
            raise ConnectionError(
                f"Failed to connect to {self.base_url}: {str(e)}"
            ) from e

        sid: str = self._search_regex(response.text, r'"FdrFJe":"([\d-]+)"', "SID")
        nonce: str = self._search_regex(response.text, r'"SNlM0e":"(.*?)"', "nonce")

        return sid, nonce

    @staticmethod
    def _search_regex(text: str, pattern: str, term: str) -> str:
        match: Optional[re.Match] = re.search(pattern, text)
        if not match:
            raise ValueError(f"Failed to extract {term}.")
        return match.group(1)

    @staticmethod
    def _get_reqid() -> int:
        return int("".join(random.choices(string.digits, k=7)))

    def _construct_params(self, sid: str) -> str:
        return urllib.parse.urlencode(
            {
                "bl": BOT_SERVER,
                "hl": os.environ.get("GEMINI_LANGUAGE", "en"),
                "_reqid": self._get_reqid(),
                "rt": "c",
                "f.sid": sid,
            }
        )

    def _construct_payload(self, prompt: str, nonce: str) -> str:
        return urllib.parse.urlencode(
            {
                "at": nonce,
                "f.req": json.dumps([None, json.dumps([[prompt], None, None])]),
            }
        )

    def send_request(self, prompt: str) -> Tuple[str, int]:
        """Sends a request and returns the response text and status code."""
        try:
            sid, nonce = self._get_sid_and_nonce()
            params = self._construct_params(sid)
            data = self._construct_payload(
                f"Provide a written response. {prompt}", nonce
            )
            response = self.session.post(
                POST_ENDPOINT,
                params=params,
                data=data,
                timeout=self.timeout,
                proxies=self.proxies,
            )
            response.raise_for_status()
            return response.text, response.status_code
        except ConnectionError as e:
            raise ConnectionError(f"Connection failed: {e}")
        except RequestException as e:
            raise RequestException(f"Request failed: {e}")

    def generate_content(self, prompt: str) -> str:
        """Generates content based on the prompt, raising an exception for non-200 responses."""
        response_text, response_status_code = self.send_request(prompt)
        if response_status_code == 200:
            return response_text
        else:
            raise ValueError(f"Response status: {response_status_code}")
