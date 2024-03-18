import os
import re
import json
import random
import string
import inspect
import requests
import urllib.parse
from typing import Optional, Tuple, Dict, Union
from requests.exceptions import ConnectionError

from .src.model.parser.custom_parser import ParseMethod1, ParseMethod2
from .src.model.parser.response_parser import ResponseParser
from .src.model.output import GeminiCandidate, GeminiModelOutput
from .src.misc.utils import upload_image
from .src.misc.constants import (
    URLs,
    Headers,
    SUPPORTED_BROWSERS,  # no-qa
)


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
        rcid (str): Response candidate ID.
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
        rcid: str = None,
    ) -> None:
        """
        Initializes the Gemini object with session, cookies, and other configurations.
        """
        self._nonce = None
        self._sid = None  # session id
        self._rcid = rcid or None  # response candidate id
        self._rid = None  # response id
        self._cid = None  # candidate id
        self.auto_cookies = auto_cookies
        self.cookie_fp = cookie_fp
        self.cookies = cookies
        self.proxies = proxies or {}
        self.timeout = timeout
        self.session = session or self._initialize_session()
        self.base_url: str = URLs.BASE_URL.value
        self.nonce = nonce
        self._reqid = int("".join(random.choices(string.digits, k=7)))
        self.parser = ResponseParser(cookies=self.cookies)

    @property
    def rcid(self):
        return self._rcid

    @rcid.setter
    def rcid(self, value):
        self._rcid = value

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
        session.headers.update(Headers.MAIN)
        if self.cookies:
            session.cookies.update(self.cookies)
        elif self.cookie_fp:
            self._set_cookies_from_file(self.cookie_fp)
        elif self.auto_cookies == True:
            self._set_cookies_automatically()

        self._set_sid_and_nonce()

        return session

    def _set_cookies_from_file(self, file_path: str) -> None:
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

    def _set_sid_and_nonce(self):
        """
        Retrieves the session ID (SID) and a SNlM0e nonce value from the application page.
        """
        try:
            response = requests.get(f"{URLs.BASE_URL.value}/app", cookies=self.cookies)
            response.raise_for_status()

            sid_match = re.search(r'"FdrFJe":"([\d-]+)"', response.text)
            nonce_match = re.search(r'"SNlM0e":"(.*?)"', response.text)

            if sid_match:
                self._sid = sid_match.group(1)
            else:
                raise ValueError(
                    "Failed to parse SID value from the response.\nRefresh the Gemini web page or access Gemini in a new incognito browser to resend cookies."
                )
            if nonce_match:
                self._nonce = nonce_match.group(1)
            else:
                raise ValueError(
                    "Failed to parse SNlM0e nonce value from the response.\nRefresh the Gemini web page or access Gemini in a new incognito browser to resend cookies."
                )

        except requests.RequestException as e:
            raise ConnectionError(f"Request failed: {e}")
        except ValueError as e:
            raise e  # Re-raise the exception after it's caught
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred: {e}")

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
                "bl": URLs.BOT_SERVER.value,
                "hl": os.environ.get("GEMINI_LANGUAGE", "en"),
                "_reqid": self._reqid,
                "rt": "c",
                "f.sid": sid,
            }
        )

    def _construct_payload(
        self, prompt: str, image: Union[bytes, str], nonce: str
    ) -> str:
        """
        Constructs URL-encoded payload for a request.

        Parameters:
            prompt (str): The user prompt to send.
            image (Union[bytes, str]): The image data as bytes or file path. Supported formats: webp, jpeg, png.
            nonce (str): A one-time token used for request verification.

        Returns:
            str: URL-encoded string of the payload.
        """
        return urllib.parse.urlencode(
            {
                "at": nonce,
                "f.req": json.dumps(
                    [
                        None,
                        json.dumps(
                            [
                                image
                                and [
                                    prompt,
                                    0,
                                    None,
                                    [[[upload_image(image), 1]]],
                                ]
                                or [prompt],
                                None,
                                [self._cid, self._rid, self._rcid],
                            ]
                        ),
                    ]
                ),
            },
        )

    def send_request(
        self, prompt: str, image: Union[bytes, str] = None
    ) -> Tuple[str, int]:
        """Sends a request and returns the response text and status code."""
        params = self._construct_params(self._sid)
        data = self._construct_payload(prompt, image, self._nonce)
        response = self.session.post(
            URLs.POST_ENDPOINT.value,
            params=params,
            data=data,
            timeout=self.timeout,
            proxies=self.proxies,
        )
        self._reqid += 100000
        response.raise_for_status()

        return response.text, response.status_code

    def generate_content(
        self, prompt: str, image: Union[bytes, str] = None
    ) -> GeminiModelOutput:
        """Generates content based on the prompt and returns a GeminiModelOutput object."""
        try:
            response_text, response_status_code = self.send_request(prompt, image)
            if response_status_code != 200:
                print(
                    f"Non-successful response status: {response_status_code}. Check Gemini session status."
                )
                return None

            parser = ResponseParser(cookies=self.cookies)
            parsed_response = parser.parse(response_text)
            return self._create_model_output(parsed_response)
        except Exception as e:
            print(
                f"Failed to generate content due to an error: {e}.\nIf the issue persists, submit it at https://github.com/dsdanielpark/Gemini-API/issues"
            )
            return None

    def _create_model_output(self, parsed_response: dict) -> GeminiModelOutput:
        """
        Creates model output from parsed response.

        Args:
            parsed_response (dict): The parsed response data.

        Returns:
            GeminiModelOutput: The model output containing metadata, candidates, and response dictionary.
        """
        candidates = self.collect_candidates(parsed_response)
        metadata = parsed_response.get("metadata", [])
        try:
            self._cid = metadata[0]
            self._rid = metadata[1]
            # self._rcid = candidates["candidates"][0]["rcid"]
        except:
            pass
        return GeminiModelOutput(
            metadata=metadata,
            candidates=candidates,
            response_dict=parsed_response,
        )

    @staticmethod
    def collect_candidates(data):
        """
        Collects candidate data from parsed response.

        Args:
            data: The parsed response data.

        Returns:
            List: A list of GeminiCandidate objects.
        """
        collected = []
        stack = [data]

        while stack:
            current = stack.pop()

            if isinstance(current, dict):
                if "rcid" in current and "text" in current:
                    collected.append(GeminiCandidate(**current))
                else:
                    stack.extend(current.values())

            elif isinstance(current, list):
                stack.extend(current)

        return collected

    # End of Code. The following codes need improvement or can be additionally used.

    def generate_custom_content(self, prompt: str, *custom_parsers) -> str:
        """Generates content based on the prompt, attempting to parse with ParseMethod1, ParseMethod2, and any additional parsers provided."""
        response_text, response_status_code = self.send_request(prompt)
        if response_status_code != 200:
            raise ValueError(f"Response status: {response_status_code}")

        parser1 = ParseMethod1()
        parser2 = ParseMethod2()
        parsers = [parser1.parse, parser2.parse]

        for custom_parser in custom_parsers:
            if inspect.isclass(custom_parser):
                instance = custom_parser()
                parsers.append(instance.parse)
            elif callable(custom_parser):
                parsers.append(custom_parser)

        for parse in parsers:
            try:
                return parse(response_text)
            except Exception as e:
                continue
        print("Parsing failed; returning original text. Consider using CustomParser.")
        return response_text

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

    # To-Do: Update cookies automatically using browser cookie3 or others.
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

    # To-Do: Get cookie values automatically.
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

    # To-Do: Get cookie values automatically.
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
