# Copyright 2024 Minwoo(Daniel) Park, MIT License, Revert checkpoint #2
import os
import re
import json
import time
import httpx
import random
import string
import asyncio
import requests
from typing import Optional, Any, List

from .constants import (
    REQUIRED_COOKIE_LIST,
    HEADERS,
    SUPPORTED_BROWSERS,
    TEXT_GENERATION_WEB_SERVER_PARAM,
    POST_ENDPOINT,
    HOST,
    Tool,
)
from .models.base import (
    GeminiOutput,
)
from .models.exceptions import (
    TimeoutError,
)


class GeminiClient:
    """
    Represents a Gemini instance for interacting with services, supporting features like automatic cookie handling, proxy configuration, Google Cloud Translation integration, and optional code execution within IPython environments.

    Attributes:
        session (requests.Session): A requests session object for making HTTP requests.
        cookies (dict): A dictionary containing cookies with their respective values. Important for maintaining session state.
        timeout (int): Request timeout in seconds. Defaults to 30.
        proxies (dict): Proxy configuration for requests. Useful for routing requests through specific network interfaces.
        language (str, optional): Natural language code for translation (e.g., "en", "ko", "ja"). Used for specifying the desired language for translation services.
        conversation_id (str, optional): An identifier for fetching conversational context. Useful in applications requiring context-aware interactions.
        auto_cookies (bool): Indicates whether to automatically retrieve and manage cookies. Defaults to False.
        google_translator_api_key (str, optional): Specifies the Google Cloud Translation API key for translation services.
        run_code (bool): Indicates whether to execute code included in the response. This is applicable only in IPython environments.
    """

    __slots__ = [
        "session",
        "token",
        "cookies",
        "timeout",
        "proxies",
        "language",
        "auto_cookies",
        "google_translator_api_key",
        "run_code",
        "share_session",
        "verify",
        "_reqid",
        "latency",
        "running"
    ]

    def __init__(
        self,
        auto_cookies: bool = False,
        token: str = None,
        session: Optional[httpx.AsyncClient] = None,
        cookies: Optional[dict] = None,
        timeout: int = 30,
        proxies: Optional[dict] = {},
        language: Optional[str] = None,
        google_translator_api_key: Optional[str] = None,
        run_code: bool = False,
        verify: bool = True,
        latency: int = 10,
        target_cookies: Optional[List] = [],
    ):
        """
        Initializes a new instance of the Gemini class, setting up the necessary configurations for interacting with the services.

        Parameters:
            auto_cookies (bool): Whether to automatically manage cookies.
            session (Optional[httpx.AsyncClient]): A custom session object. If not provided, a new session will be created.
            cookies (Optional[dict]): Initial cookie values. If auto_cookies is True, cookies are managed automatically.
            timeout (int): Request timeout in seconds. Defaults to 30.
            proxies (Optional[dict]): Proxy configurations for the requests.
            language (Optional[str]): Default language for translation services.
            conversation_id (Optional[str]): ID for fetching conversational context.
            google_translator_api_key (Optional[str]): Google Cloud Translation API key.
            run_code (bool): Flag indicating whether to execute code in IPython environments.
        """
        self.auto_cookies = auto_cookies
        self.target_cookies = target_cookies
        self.latency = latency
        self.running = False
        self._reqid = int("".join(random.choices(string.digits, k=4)))
        self.cookies = cookies or {}
        self._get_cookies(auto_cookies)
        self.proxies = proxies or {}
        self.timeout = timeout
        self.session = session
        self.token = token
        self.token = self.get_nonce_value()
        self.language = language or os.getenv("GEMINI_LANGUAGE")
        self.google_translator_api_key = google_translator_api_key
        self.run_code = run_code
        self.verify = verify
        

    async def async_init(self, auto_close: bool = False, close_delay: int = 300):
        self.session = await self._create_async_session(auto_close = auto_close, close_delay = close_delay)

    async def close_session(self):
        if self.session:
            await self.session.aclose()
            self.session = None
            self.running = False

    async def reset_close_task(self) -> None:
        if self.close_task:
            self.close_task.cancel()
            self.close_task = None
        self.close_task = asyncio.create_task(self.close())

    def check_session_cookies(self):
        if self.session:
            cookies = self.session.cookies.get_dict()
            cookies_str = "\n".join(
                [f"{key}: {value}" for key, value in cookies.items()]
            )
            print("Session Cookies:\n" + cookies_str)

    def check_session_cookies(self):
        if self.session:
            cookies_str = "\n".join(
                [f"{key}: {value}" for key, value in self.session.cookies.items()]
            )
            print("Session Cookies:\n" + cookies_str)
        else:
            print("Session not initialized.")

    def check_client_headers(self):
        """Prints the current session's headers"""
        if self.session:
            headers = self.session.headers
            headers_str = "\n".join(
                [f"{key}: {value}" for key, value in headers.items()]
            )
            print("Session Headers:\n" + headers_str)
        else:
            print("Session not initialized.")

    def _get_cookies_from_browser(self) -> dict:
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
                print(
                    f"Automatically configure cookies with detected ones.\n{found_cookies}"
                )
                self.cookies = found_cookies

            except Exception as e:
                continue  # Ignore exceptions and try the next browser function

        if not self.cookies:
            raise ValueError(
                "Failed to get cookies. Set 'cookies' argument or 'auto_cookies' as True."
            )
        required_cookie_set = set(REQUIRED_COOKIE_LIST)
        current_cookie_keys = set(self.cookies.keys())
        if not required_cookie_set.issubset(current_cookie_keys):
            print(
                "Some recommended cookies not found: 'SIDCC' or '__Secure-1PSIDTS', '__Secure-1PSIDCC', '__Secure-1PSID', and 'NID'.\nIt depends on your Contries/Legions."
            )

    def _get_cookies(self, auto_cookies: bool) -> None:
        """
        Updates the instance's cookies attribute with Gemini API tokens, either from environment variables or by extracting them from the browser, based on the auto_cookies flag.
        """
        # Initialize cookies dictionary if not already initialized
        if not hasattr(self, "cookies"):
            self.cookies = {}

        # Load cookies from environment variables
        env_cookies = {
            cookie: os.getenv(cookie)
            for cookie in REQUIRED_COOKIE_LIST
            if os.getenv(cookie)
        }
        self.cookies.update(env_cookies)

        # Attempt to load cookies automatically from the browser if necessary
        if auto_cookies and not self.cookies:
            try:
                self._get_cookies_from_browser()
            except Exception as e:
                raise Exception("Failed to extract cookies from browser.") from e

        # Warning if no cookies are available
        if not auto_cookies and not self.cookies:
            print(
                "Cookie loading issue, try setting auto_cookies to True. Restart browser, log out, log in for Gemini Web UI to work. Keep a single browser open."
            )
            try:
                self.auto_cookies = True
                self._get_cookies_from_browser()

            except Exception as e:
                print(e)

        # Raise an exception if still no cookies
        if not self.cookies:
            raise Exception(
                "Gemini cookies must be provided through environment variables or extracted from the browser with auto_cookies enabled."
            )

    async def _create_async_session(self, auto_close: bool, close_delay: int) -> httpx.AsyncClient:
        """
        Initializes or configures the httpx.AsyncClient session with predefined session headers, proxies, and cookies.

        Returns:
            httpx.AsyncClient: The session object, configured with headers, proxies, and cookies.

        Raises:
            ValueError: If the 'cookies' dictionary is empty, indicating that there's insufficient information to properly set up a new session.
        """
        if self.session is not None:
            return self.session

        if not self.cookies:
            raise ValueError("Failed to set session. 'cookies' dictionary is empty.")

        self.session = httpx.AsyncClient(
            headers=HEADERS,
            cookies=self.cookies,
            proxies=self.proxies,
            timeout=self.timeout,
        )

        # Ensure session is initialized
        if not hasattr(self, "session") or self.session is None:
            for i in range(2):
                print(f"Re-try to create async client. ({i})")
                try:
                    self.session = httpx.AsyncClient(
                        headers=HEADERS,
                        cookies=self.cookies,
                        proxies=self.proxies,
                        timeout=self.timeout,
                    )
                    self.auto_close = auto_close
                    self.close_delay = close_delay
                    if self.auto_close:
                        await self.reset_close_task()
                except Exception as e:
                    await self.close(0)
                    print(e)
                    raise
        if hasattr(self, "session"):
            self.running = True
        else:
            self.running = False

        return self.session
    


    async def update_target_cookies(self, target_cookies: dict = None):
        """
        Updates specified cookies in the httpx client. If target_cookies is not provided,
        updates all cookies stored in self.cookies.

        Parameters:
        - target_cookies (dict, optional): A dictionary of cookie names and values to update.
                                           If None, updates all cookies from self.cookies.
        """
        cookies_to_update = target_cookies if target_cookies is not None else self.cookies

        self._get_cookies(True)

        try:
            for cookie_name, cookie_value in cookies_to_update.items():
                if cookie_value:
                    self.session.cookies.set(cookie_name, cookie_value)
                else:
                    print(f"Warning: Cookie value for {cookie_name} is missing; skipping update.")
        except Exception as e:
            print(f"An error occurred while updating cookies: {e}")

    def get_nonce_value(self) -> str:
        """
        Get the Nonce Token value from the Gemini API response.
        """
        error_message = "Nonce token value not found or response status is not 200."

        with requests.Session() as session:
            response = session.get(HOST, timeout=self.timeout, proxies=self.proxies)
            if response.status_code == 200:
                match = re.search(r'nonce="([^"]+)"', response.text)
                if match:
                    return match.group(1)
            raise Exception(error_message)
    
    def _prepare_data(self, prompt: str, gemini_session: Optional["GeminiSession"] = None) -> dict:
        session_metadata = gemini_session.metadata if gemini_session and gemini_session.metadata else None
        request_body = [None, [[prompt], None, session_metadata]]
        
        data = {
            "at": self.token,
            "f.req": json.dumps([None, json.dumps(request_body)]),
        }
        return data
    
    def _prepare_params(self) -> dict:
        return {
            "bl": TEXT_GENERATION_WEB_SERVER_PARAM,
            "_reqid": str(self._reqid),
            "rt": "c",
        }

    async def post_prompt(self, prompt: str, gemini_session: Optional["GeminiSession"] = None) -> dict:
        data = self._prepare_data(prompt, gemini_session)
        params = self._prepare_params()

        response = await self.session.post(
            POST_ENDPOINT,
            data=data,
            params=params,
            timeout=self.timeout,
        )
        self._reqid += 100000

        return response

    async def _post_initial_prompt(self, prompt: str) -> dict:
        """Sends the initial prompt request and returns the response."""
        response = await self.post_prompt(prompt)
        await asyncio.sleep(self.latency)
        print(f"Initial request status: {response.status_code}")
        return response

    async def attempt_fetch_with_retries(self, prompt: str, wait_time: int = 40) -> dict:
        """Attempts to fetch the content with retries until a status code 200 is received or a timeout occurs."""
        try:
            request_batch_execute = await self._post_initial_prompt(prompt)
            await asyncio.sleep(self.latency)
            await self.update_target_cookies(self.target_cookies)
            async def attempt_fetch():
                nonlocal request_batch_execute
                while True:
                    response = await self.post_prompt(prompt)
                    print(f"Current batch execution status: {response.status_code}")
                    if response.status_code == 200:
                        print("Received status code 200. Processing response.")
                        return response
                    else:
                        request_batch_execute = response
                        await asyncio.sleep(self.latency)

            return await asyncio.wait_for(attempt_fetch(), timeout=wait_time)
        except asyncio.TimeoutError:
            print(f"Timeout: Did not receive status code 200 within {wait_time} seconds. Returning last response.")
            return request_batch_execute
        except asyncio.CancelledError as e:
            print(f"Operation was cancelled due to: {e}. Handling cleanup here if necessary.")
            return request_batch_execute
        except Exception as e:
            raise Exception(f"Failed to process request: {e}")



    async def request_share(
        self,
        session: Optional["GeminiSession"] = None,
    ) -> dict:
        """
        Asynchronously generates content by querying the Gemini API, supporting text and optional image input alongside a specified tool for content generation.

        Args:
            session (Optional[GeminiSession]): A session object for the Gemini API, if None, a new session is created or a default session is used.

        Returns:
            dict: A dictionary containing the response from the Gemini API.
        """
        url = "https://clients6.google.com/upload/drive/v3/files?uploadType=multipart&fields=id&key=AIzaSyAHCfkEDYwQD6HuUx2DyX3VylTrKZG7doM"

        # Use httpx.ClientSession for asynchronous HTTP requests
        async with httpx.AsyncClient() as session:
            try:
                async with session.post(url, timeout=self.timeout) as response:
                    return await response.json()
            except asyncio.TimeoutError:
                raise TimeoutError(
                    "Request timed out. If errors persist, increase the timeout parameter in the Gemini class to a higher number of seconds."
                )


class GeminiSession:
    """
    Represents a session to manage and retrieve conversation history in the context of Gemini services. This class facilitates interaction with the Gemini API, allowing for the retrieval of conversation history based on specified metadata identifiers.

    Attributes:
        gemini (Gemini): An instance of the Gemini client interface used for interactions with https://gemini.google.com/. This attribute is essential for making API calls and retrieving data.
        __metadata (list[str], optional): A list of strings representing chat metadata, potentially including chat ID (`cid`), reply ID (`rid`), and reply candidate ID (`rcid`). This list can vary in length, accommodating fewer than three elements to match provided identifiers.
        gemini_output: Stores the output from the Gemini API calls. This attribute is managed internally and populated based on interactions facilitated by the session.

    Parameters:
        gemini (Gemini): The Gemini client interface, providing the necessary functionality to interact with the Gemini API.
        metadata (list[str], optional): A list containing identifiers for chat metadata, such as `[cid, rid, rcid]`. The list can be shorter, with one or two elements like `[cid]` or `[cid, rid]`, depending on the available information.
        cid (str, optional): A specific chat ID. If provided along with `metadata`, it will replace the first element in the metadata list, signifying the chat ID.
        rid (str, optional): A specific reply ID. If provided along with `metadata`, it will replace the second element in the metadata list, indicating the reply ID.
        rcid (str, optional): A specific reply candidate ID. If provided along with `metadata`, it will replace the third element in the metadata list, denoting the reply candidate ID.

    The class requires a Gemini instance to function correctly. It uses the provided metadata, along with optional specific identifiers (`cid`, `rid`, `rcid`), to manage and retrieve conversation history. Only when all three identifiers are provided will the complete conversation history be retrieved.
    """

    __slots__ = ["__metadata", "gemini", "gemini_output"]

    def __init__(
        self,
        gemini: GeminiClient,
        metadata: Optional[List[str]] = None,
        cid: Optional[str] = None,  # chat id
        rid: Optional[str] = None,  # reply id
        rcid: Optional[str] = None,  # reply candidate id
    ):
        self.__metadata: list[Optional[str]] = [None, None, None]
        self.gemini: GeminiClient = gemini
        self.gemini_output: Optional[GeminiOutput] = None

        if metadata:
            self.metadata = metadata
        if cid:
            self.cid = cid
        if rid:
            self.rid = rid
        if rcid:
            self.rcid = rcid

    def __str__(self):
        return f"GeminiSession(cid='{self.cid}', rid='{self.rid}', rcid='{self.rcid}')"

    __repr__ = __str__

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        if name == "gemini_output" and isinstance(value, GeminiOutput):
            self.metadata = value.metadata
            self.rcid = value.rcid

    def send_message(self, prompt: str) -> GeminiOutput:
        """
        Generates content by submitting a prompt to the Gemini API, acting as a shortcut method for `Gemini.generate_content(prompt, self)`.

        This method simplifies the process of content generation by directly accepting a user-provided prompt and leveraging the Gemini API to generate relevant content. The output encompasses a variety of content forms, including text responses, images, and a list of all answer candidates.

        Parameters:
            prompt (str): The input text provided by the user, serving as the basis for content generation.

        Returns:
            GeminiOutput: An object encapsulating the output data from gemini.google.com. The `GeminiOutput` object offers several attributes for accessing different parts of the response:
                - `text` for retrieving the default text reply.
                - `images` for obtaining a list of images included in the default reply.
                - `candidates` for accessing a comprehensive list of all answer candidates within the gemini_output.

        The method ensures a streamlined interface for interacting with the Gemini API, facilitating the retrieval of diverse content types based on the input prompt.
        """
        return self.gemini.generate_content(prompt, self)

    def choose_candidate(self, index: int) -> GeminiOutput:
        """
        Selects a specific candidate from the most recent `GeminiOutput` to direct the flow of an ongoing conversation.

        This method allows the user to influence the direction of the conversation by choosing one of the answer candidates provided by the last Gemini API call. By specifying the index of the desired candidate, the conversation can be steered towards a particular topic or response style.

        Parameters:
            index (int): The zero-based index of the candidate to be selected. This index corresponds to the position of the candidate within the list of answer candidates provided in the last `GeminiOutput`.

        The chosen candidate will affect subsequent interactions with the Gemini API, guiding the content and responses generated based on the selected conversational path.
        """
        if not self.gemini_output:
            raise ValueError(
                "No previous gemini_output data found in this chat session."
            )

        self.gemini_output.chosen = index
        self.rcid = self.gemini_output.rcid
        return self.gemini_output

    @property
    def metadata(self):
        return self.__metadata

    @metadata.setter
    def metadata(self, value: List[str]):
        if len(value) > 3:
            raise ValueError("metadata cannot exceed 3 elements")
        self.__metadata[: len(value)] = value

    @property
    def cid(self):
        return self.__metadata[0]

    @cid.setter
    def cid(self, value: str):
        self.__metadata[0] = value

    @property
    def rid(self):
        return self.__metadata[1]

    @rid.setter
    def rid(self, value: str):
        self.__metadata[1] = value

    @property
    def rcid(self):
        return self.__metadata[2]

    @rcid.setter
    def rcid(self, value: str):
        self.__metadata[2] = value


def running(func) -> callable:
    async def wrapper(self: "GeminiClient", *args, **kwargs):
        if not self.running:
            await self.init(auto_close=self.auto_close, close_delay=self.close_delay)
            if self.running:
                return await func(self, *args, **kwargs)

            raise Exception(
                f"Invalid function call: GeminiClient.{func.__name__}. Client initialization failed."
            )
        else:
            return await func(self, *args, **kwargs)

    return wrapper
