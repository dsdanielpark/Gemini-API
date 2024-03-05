# Copyright 2024 Daniel Park, Antonio Cheang, MIT License
import os
import re
import json
import random
import string
import requests
import urllib.parse
from typing import Optional, Tuple, Dict
from requests.exceptions import ConnectionError, RequestException

from .models.parser.methods import ParseMethod1, ParseMethod2
from .constants import HEADERS, HOST, BOT_SERVER, POST_ENDPOINT, SUPPORTED_BROWSERS


class Gemini:
    """
    A class to manage interactions with a web service, handling sessions, cookies, and proxies.

    Attributes:
        auto_cookies (bool): Whether to automatically manage cookies.
        cookies (Dict[str, str]): A dictionary of cookies.
        proxies (dict): A dictionary of proxy settings.
        timeout (int): The timeout for requests.
        session (requests.Session): The session for making requests.
        base_url (str): The base URL for the web service.

    Parameters:
        session (Optional[requests.Session]): An existing requests session, if any.
        cookies (Optional[Dict[str, str]]): Initial cookies to use, if any.
        cookie_fp (str): File path to load cookies from, if `auto_cookies` is True.
        auto_cookies (bool): Automatically manage cookies if True.
        timeout (int): Timeout for requests, defaults to 30 seconds.
        proxies (Optional[dict]): Proxy configuration for requests, if any.
    """

    def __init__(
        self,
        session: Optional[requests.Session] = None,
        cookies: Optional[Dict[str, str]] = None,
        nonce: Optional[str] = None,
        cookie_fp: str = None,
        auto_cookies: bool = False,
        timeout: int = 30,
        proxies: Optional[dict] = None,
    ) -> None:
        """
        Initializes the Gemini object with session, cookies, and other configurations.
        """
        self._nonce = None
        self._sid = None
        self.auto_cookies = auto_cookies
        self.cookie_fp = cookie_fp
        self.cookies = cookies
        self.proxies = proxies or {}
        self.timeout = timeout
        self.session = session or self._initialize_session()
        self.base_url: str = HOST
        self.nonce = nonce

    def _initialize_session(
        self,
    ) -> requests.Session:
        """
        Initializes a new session with headers, cookies, and optionally loads cookies from a file.

        Parameters:
            cookies (Optional[Dict[str, str]]): Cookies to add to the session.
            cookie_fp (Optional[str]): Path to a file from which to load cookies.

        Returns:
            requests.Session: The initialized session.
        """
        session = requests.Session()
        session.headers.update(HEADERS)
        if self.cookies:
            session.cookies.update(self.cookies)
        elif self.cookie_fp:
            self._load_cookies_from_file(self.cookie_fp)
        elif self.auto_cookies == True:
            self._set_cookies_automatically()

        self._set_sid_and_nonce()

        return session

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
            else:
                with open(file_path, "r") as file:
                    content = file.read()
                    try:
                        cookies = eval(content)
                    except NameError:
                        cookies = json.loads(content.replace("'", '"'))
            self.session.cookies.update(cookies)
        except Exception as e:
            print(f"Error loading cookie file: {e}")

    def _set_cookies_automatically(self) -> None:
        """
        Updates the instance's cookies attribute with Gemini API tokens, either from environment variables or by extracting them from the browser, based on the auto_cookies flag.
        """
        if len(getattr(self, "cookies", {})) > 5:
            return

        if self.auto_cookies:
            try:
                self._update_cookies_from_browser()
                if not self.cookies:
                    raise ValueError("No cookies were loaded from the browser.")
            except Exception as e:
                raise Exception("Failed to extract cookies from browser.") from e
        else:
            print(
                "Cookie loading issue, try setting auto_cookies to True. Restart browser, log out, log in for Gemini Web UI to work. Keep a single browser open."
            )
            try:
                self.auto_cookies = True
                self._update_cookies_from_browser()
                if not self.cookies:
                    raise ValueError("No cookies were loaded from the browser.")
            except Exception as e:
                print(f"Automatic cookie retrieval failed: {e}")

        if not self.cookies:
            raise Exception(
                "Gemini cookies must be provided through environment variables or extracted from the browser with auto_cookies enabled."
            )

    def _update_cookies_from_browser(self) -> dict:
        """
        Attempts to extract specific Gemini cookies from the cookies stored by web browsers on the current system.

        This method iterates over a predefined list of supported browsers, attempting to retrieve cookies that match a specific domain (e.g., ".google.com"). If the required cookies are found, they are added to the instance's cookie store. The process supports multiple modern web browsers across different operating systems.

        The method updates the instance's `cookies` attribute with any found cookies that match the specified criteria.

        Raises:
            ValueError: If no supported browser is found with the required cookies, or if an essential cookie is missing after attempting retrieval from all supported browsers.
        """

        for browser_fn in SUPPORTED_BROWSERS:
            try:
                print(
                    f"Trying to automatically retrieve cookies from {browser_fn} using the browser_cookie3 package."
                )
                cj = browser_fn(domain_name=".google.com")
                found_cookies = {cookie.name: cookie.value for cookie in cj}
                if len(found_cookies) >= 5:
                    print(
                        f"Successfully retrieved cookies from {browser_fn}.\n{found_cookies}"
                    )
                    self.cookies = found_cookies
                    break
                else:
                    print(
                        f"Automatically configure cookies with detected ones but found only {len(found_cookies)} cookies.\n{found_cookies}"
                    )
            except Exception as e:
                print(e)
                continue

        if not self.cookies:
            raise ValueError(
                "Failed to get cookies. Set 'cookies' argument or 'auto_cookies' as True."
            )

    def _set_sid_and_nonce(self):
        """
        Retrieves the session ID (SID) and a SNlM0e nonce value from the application page.
        """
        url = f"{HOST}/app"
        response = requests.get(url, cookies=self.cookies)
        self._sid = re.search(r'"FdrFJe":"([\d-]+)"', response.text).group(1)
        self._nonce = re.search(r'"SNlM0e":"(.*?)"', response.text).group(1)

    # def _set_sid_and_nonce(self) -> Tuple[str, str]:
    #     """
    #     Retrieves the session ID (SID) and a SNlM0e nonce value from the application page.
    #     """
    #     url = f"{HOST}/app"
    #     try:
    #         response = requests.get(
    #             url, cookies=self.cookies
    #         )
    #         sid_match, nonce_match = self.extract_sid_nonce(response.text)

    #         if not sid_match or not nonce_match:
    #             print(
    #                 "Failed to get SID or nonce. Trying to update cookies automatically..."
    #             )
    #             self._set_cookies_automatically()
    #             response = requests.get(
    #                 url, cookies=self.cookies
    #             )
    #             sid_match, nonce_match = self.extract_sid_nonce(response.text)

    #             if not nonce_match:
    #                 if self.nonce:
    #                     return (sid_match, self.nonce)
    #                 else:
    #                     raise Exception(
    #                         "Can not retrieve SID and nonce even after automatic cookie update."
    #                     )
    #         return (sid_match.group(1), nonce_match.group(1))

    #     except Exception as e:
    #         raise ConnectionError(
    #             f"Failed to retrive SID or Nonce valuse:\n{e}"
    #         )

    @staticmethod
    def extract_sid_nonce(response_text):
        sid_match = re.search(r'"FdrFJe":"([\d-]+)"', response_text)
        nonce_match = re.search(r'"SNlM0e":"(.*?)"', response_text)
        return sid_match, nonce_match

    @staticmethod
    def get_reqid() -> int:
        """
        Generates a random 7-digit request ID.

        Returns:
            int: A random 7-digit integer used as a request ID.
        """
        return int("".join(random.choices(string.digits, k=7)))

    def _construct_params(self, sid: str) -> str:
        """
        Constructs URL-encoded parameters for a request.

        Parameters:
            sid (str): The session ID.

        Returns:
            str: URL-encoded string of parameters.
        """
        return urllib.parse.urlencode(
            {
                "bl": BOT_SERVER,
                "hl": os.environ.get("GEMINI_LANGUAGE", "en"),
                "_reqid": self.get_reqid(),
                "rt": "c",
                "f.sid": sid,
            }
        )

    def _construct_payload(self, prompt: str, nonce: str) -> str:
        """
        Constructs URL-encoded payload for a request.

        Parameters:
            prompt (str): The user prompt to send.
            nonce (str): A one-time token used for request verification.

        Returns:
            str: URL-encoded string of the payload.
        """
        return urllib.parse.urlencode(
            {
                "at": nonce,
                "f.req": json.dumps([None, json.dumps([[prompt], None, None])]),
            }
        )

    def send_request(self, prompt: str) -> Tuple[str, int]:
        """Sends a request and returns the response text and status code."""
        try:
            params = self._construct_params(self._sid)
            data = self._construct_payload(prompt, self._nonce)
            response = self.session.post(
                POST_ENDPOINT,
                params=params,
                data=data,
                timeout=self.timeout,
                proxies=self.proxies,
            )
            response.raise_for_status()
        except (ConnectionError, RequestException) as e:
            print(f"Retry to generate content: {e}")
            # self._update_cookies_from_browser()
            self._set_sid_and_nonce()
            params = self._construct_params(self._sid)
            data = self._construct_payload(prompt, self._nonce)
            response = self.session.post(
                POST_ENDPOINT,
                params=params,
                data=data,
                timeout=self.timeout,
                proxies=self.proxies,
            )
            if response.status_code != 200:
                self.auto_cookies = False
                print(
                    "Re-try to generate content failed. Update cookie values manually."
                )
            response.raise_for_status()
        return response.text, response.status_code

    def generate_content(self, prompt: str, *custom_parsers) -> str:
        """Generates content based on the prompt, attempting to parse with ParseMethod1, ParseMethod2, and any additional parsers provided."""
        response_text, response_status_code = self.send_request(prompt)
        if response_status_code != 200:
            raise ValueError(f"Response status: {response_status_code}")

        parsers = [ParseMethod1.parse, ParseMethod2.parse] + list(custom_parsers)
        for parse in parsers:
            try:
                return parse(response_text)
            except Exception as e:
                continue
        print("Parsing failed; returning original text. Consider using CustomParser.")
        return response_text
