# Copyright 2024 Minwoo(Daniel) Park, MIT License
import os
import re
import json
import base64
import requests
import aiohttp
import asyncio
from typing import Optional, Any, List

try:
    from deep_translator import GoogleTranslator
    from google.cloud import translate_v2 as translate
except ImportError:
    pass

from .constants import (
    ALLOWED_LANGUAGES,
    REQUIRED_COOKIE_LIST,
    HEADERS,
    SHARE_HEADERS,
    TEXT_GENERATION_WEB_SERVER_PARAM,
    SUPPORTED_BROWSERS,
    Tool,
)
from .models.base import (
    GeminiOutput,
)
from .models.exceptions import (
    TimeoutError,
)


class Gemini:
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
        "conversation_id",
        "auto_cookies",
        "google_translator_api_key",
        "run_code",
        "share_session",
        "verify",
    ]

    def __init__(
        self,
        auto_cookies: bool = False,
        token: str = None,
        session: Optional[requests.Session] = None,
        share_session: Optional[requests.Session] = None,
        cookies: Optional[dict] = None,
        timeout: int = 30,
        proxies: Optional[dict] = None,
        language: Optional[str] = None,
        conversation_id: Optional[str] = None,
        google_translator_api_key: Optional[str] = None,
        run_code: bool = False,
        verify: bool = True,
    ):
        """
        Initializes a new instance of the Gemini class, setting up the necessary configurations for interacting with the services.

        Parameters:
            auto_cookies (bool): Whether to automatically manage cookies.
            session (Optional[requests.Session]): A custom session object. If not provided, a new session will be created.
            cookies (Optional[dict]): Initial cookie values. If auto_cookies is True, cookies are managed automatically.
            timeout (int): Request timeout in seconds. Defaults to 30.
            proxies (Optional[dict]): Proxy configurations for the requests.
            language (Optional[str]): Default language for translation services.
            conversation_id (Optional[str]): ID for fetching conversational context.
            google_translator_api_key (Optional[str]): Google Cloud Translation API key.
            run_code (bool): Flag indicating whether to execute code in IPython environments.
        """
        self.auto_cookies = auto_cookies
        self.cookies = cookies or {}
        self._set_cookies(auto_cookies)
        self.proxies = proxies or {}
        self.timeout = timeout
        self.session = self._set_session(session)
        self.share_session = self._set_share_session(share_session)
        self.token = token
        self.token = self._get_token()
        self.conversation_id = conversation_id or ""
        self.language = language or os.getenv("GEMINI_LANGUAGE")
        self.google_translator_api_key = google_translator_api_key
        self.run_code = run_code
        self.verify = verify

    def check_session_cookies(self):
        """Prints the current session's cookies with each key-value pair on a new line."""
        if self.session:
            cookies = self.session.cookies.get_dict()
            cookies_str = "\n".join([f"{key}: {value}" for key, value in cookies.items()])
            print("Session Cookies:\n" + cookies_str)
        else:
            print("Session not initialized.")

    def check_session_headers(self):
        """Prints the current session's headers with each key-value pair on a new line."""
        if self.session:
            headers = self.session.headers
            headers_str = "\n".join([f"{key}: {value}" for key, value in headers.items()])
            print("Session Headers:\n" + headers_str)
        else:
            print("Session not initialized.")

    def _set_cookies_from_browser(self) -> None:
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
                
                self.cookies.update(found_cookies)
                print(f"Automatically configure cookies with detected ones.\n{found_cookies}")
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
                "Some recommended cookies not found: '__Secure-1PSIDTS', '__Secure-1PSIDCC', '__Secure-1PSID', and 'NID'."
            )

    def _set_cookies(self, auto_cookies: bool) -> None:
        """
        Updates the instance's cookies attribute with Gemini API tokens, either from environment variables or by extracting them from the browser, based on the auto_cookies flag.

        Args:
            auto_cookies (bool): Indicates whether to attempt automatic extraction of tokens from the browser's cookies.

        Raises:
            Exception: If no cookies are provided through environment variables or cannot be extracted from the browser when auto_cookies is True.
        """
        if not self.cookies:
            self.cookies.update(
                {
                    cookie: os.getenv(cookie)
                    for cookie in REQUIRED_COOKIE_LIST
                    if os.getenv(cookie)
                }
            )

        if auto_cookies and not self.cookies:
            try:
                self._set_cookies_from_browser()  # Assuming this updates self.cookies directly
            except (
                Exception
            ) as e:  # Consider specifying more precise exceptions if possible
                raise Exception("Failed to extract cookies from browser.") from e
        if not auto_cookies and not self.cookies:
            print(
                "Cookie loading issue, try setting auto_cookies to True. Restart browser, log out, log in for Gemini Web UI to work. Keep a single browser open."
            )
        if not self.cookies:
            raise Exception(
                "Gemini cookies must be provided through environment variables or extracted from the browser with auto_cookies enabled."
            )
        

    def _set_session(
        self, session: Optional[requests.Session] = None
    ) -> requests.Session:
        """
        Initializes or uses a provided requests.Session object. If a session is not provided, a new one is created.
        The new or provided session is configured with predefined session headers, proxies, and cookies from the instance.

        Args:
            session (Optional[requests.Session]): An optional requests.Session object. If provided, it will be used as is; otherwise, a new session is created.

        Returns:
            requests.Session: The session object, either the one provided or a newly created and configured session.

        Raises:
            ValueError: If 'session' is None and the 'cookies' dictionary is empty, indicating that there's insufficient information to properly set up a new session.
        """
        if session is not None:
            return session

        if not self.cookies:
            raise ValueError("Failed to set session. 'cookies' dictionary is empty.")

        session = requests.Session()
        session.headers.update(
            HEADERS
        )  # Use `update` to ensure we're adding to any existing headers
        session.proxies.update(self.proxies)  # Similarly, use `update` for proxies
        session.cookies.update(self.cookies)

        return session
    
    def _set_share_session(
        self, session: Optional[requests.Session] = None
    ) -> requests.Session:
        """
        Initializes or uses a provided requests.Session object. If a session is not provided, a new one is created.
        The new or provided session is configured with predefined session headers, proxies, and cookies from the instance.

        Args:
            session (Optional[requests.Session]): An optional requests.Session object. If provided, it will be used as is; otherwise, a new session is created.

        Returns:
            requests.Session: The session object, either the one provided or a newly created and configured session.

        Raises:
            ValueError: If 'session' is None and the 'cookies' dictionary is empty, indicating that there's insufficient information to properly set up a new session.
        """
        if session is not None:
            return session

        if not self.cookies:
            raise ValueError("Failed to set session. 'cookies' dictionary is empty.")

        session = requests.Session()
        session.headers.update(
            SHARE_HEADERS
        )  # Use `update` to ensure we're adding to any existing headers
        session.proxies.update(self.proxies)  # Similarly, use `update` for proxies
        session.cookies.update(self.cookies)

        return session

    def _get_token(self) -> str:
        """
        Get the SNlM0e Token value from the Gemini API response.

        Returns:
            str: SNlM0e token value.
        Raises:
            Exception: If the __Secure-1PSID value is invalid or token value is not found in the response.
        """
        response = self.session.get(
            "https://gemini.google.com/", timeout=self.timeout, proxies=self.proxies
        )
        if response.status_code != 200:
            raise Exception(
                f"Response status code is not 200. Response Status is {response.status_code}"
            )
        nonce = re.findall(r'nonce="([^"]+)"', response.text)
        if nonce == None:
            raise Exception(
                "SNlM0e token value not found. Double-check cookies dict value or set 'auto_cookies' parametes as True.\nOccurs due to cookie changes. Re-enter new cookie, restart browser, re-login, or manually refresh cookie."
            )
        return nonce

    def _post_prompt(
        self,
        prompt: str,
        session: Optional["GeminiSession"] = None,
    ) -> dict:
        """
        Generates content by querying the Gemini API, supporting text and optional image input alongside a specified tool for content generation.

        Args:
            prompt (str): The input text for the content generation query.
            session (Optional[GeminiSession]): A session object for the Gemini API, if None, a new session is created or a default session is used.
            image (Optional[bytes]): Input image bytes for the query; supported image types include JPEG, PNG, and WEBP. This parameter is optional and used for queries that benefit from image context.
            tool (Optional[Tool]): The tool to use for content generation, specifying the context or platform for which the content is relevant. Options include Gmail, Google Docs, Google Drive, Google Flights, Google Hotels, Google Maps, and YouTube. This parameter is optional.

        Returns:
            dict: A dictionary containing the response from the Gemini API, which may include content, conversation ID, response ID, factuality queries, text query, choices, links, images, programming language, code, and status code.
        """
        data = {
            "at": self.token,
            "f.req": json.dumps(
                [None, json.dumps([[prompt], None, session and session.metadata])]
            ),
            "rpcids": "ESY5D"
        }

        # Post request that cannot receive any response due to Google changing the logic for the Gemini API Post to the Web UI.
        try:
            _post_prompt_response = self.session.post(
                "https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate",
                data=data,
                timeout=self.timeout,
                proxies=self.proxies,
                verify=self.verify,
            )
        except:
            raise TimeoutError(
                "Request timed out. If errors persist, increase the timeout parameter in the Gemini class to a higher number of seconds."
            )
        
        return _post_prompt_response
    
    def _request_copy_to_clipboard(
        self,
        prompt: str,
        session: Optional["GeminiSession"] = None,
    ) -> dict:
        """
        Generates content by querying the Gemini API, supporting text and optional image input alongside a specified tool for content generation.

        Args:
            prompt (str): The input text for the content generation query.
            session (Optional[GeminiSession]): A session object for the Gemini API, if None, a new session is created or a default session is used.
            image (Optional[bytes]): Input image bytes for the query; supported image types include JPEG, PNG, and WEBP. This parameter is optional and used for queries that benefit from image context.
            tool (Optional[Tool]): The tool to use for content generation, specifying the context or platform for which the content is relevant. Options include Gmail, Google Docs, Google Drive, Google Flights, Google Hotels, Google Maps, and YouTube. This parameter is optional.

        Returns:
            dict: A dictionary containing the response from the Gemini API, which may include content, conversation ID, response ID, factuality queries, text query, choices, links, images, programming language, code, and status code.
        """
        data = {
            "at": self.token,
        }

        # Post request that cannot receive any response due to Google changing the logic for the Gemini API Post to the Web UI.
        try:
            _request_copy_to_clipboard_response = self.session.post(
                "https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate",
                data=data,
                timeout=self.timeout,
                proxies=self.proxies,
                verify=self.verify,
            )
        except:
            raise TimeoutError(
                "Request timed out. If errors persist, increase the timeout parameter in the Gemini class to a higher number of seconds."
            )
        
        return _request_copy_to_clipboard_response
    

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
            
            # Use aiohttp.ClientSession for asynchronous HTTP requests
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.post(url, timeout=self.timeout) as response:
                        return await response.json()
                except asyncio.TimeoutError:
                    raise TimeoutError(
                        "Request timed out. If errors persist, increase the timeout parameter in the Gemini class to a higher number of seconds."
                    )
        
    def _post_conversation(
        self,
        prompt: str,
        session: Optional["GeminiSession"] = None,
    ) -> dict:
        """
        Generates content by querying the Gemini API, supporting text and optional image input alongside a specified tool for content generation.

        Args:
            prompt (str): The input text for the content generation query.
            session (Optional[GeminiSession]): A session object for the Gemini API, if None, a new session is created or a default session is used.
            image (Optional[bytes]): Input image bytes for the query; supported image types include JPEG, PNG, and WEBP. This parameter is optional and used for queries that benefit from image context.
            tool (Optional[Tool]): The tool to use for content generation, specifying the context or platform for which the content is relevant. Options include Gmail, Google Docs, Google Drive, Google Flights, Google Hotels, Google Maps, and YouTube. This parameter is optional.

        Returns:
            dict: A dictionary containing the response from the Gemini API, which may include content, conversation ID, response ID, factuality queries, text query, choices, links, images, programming language, code, and status code.
        """
        data = {
            "at": self.token,
            "f.req": json.dumps(
                [None, json.dumps([[prompt], None, session and session.metadata])]
            ),
        }

        # Post request that cannot receive any response due to Google changing the logic for the Gemini API Post to the Web UI.
        try:
            _post_conversation_response = self.session.post(
                "https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate",
                data=data,
                timeout=self.timeout,
                proxies=self.proxies,
            )
        except:
            raise TimeoutError(
                "Request timed out. If errors persist, increase the timeout parameter in the Gemini class to a higher number of seconds."
            )
        
        return _post_conversation_response



    def generate_content(
        self,
        prompt: str,
        session: Optional["GeminiSession"] = None,
        image: Optional[bytes] = None,
        tool: Optional[Tool] = None,
    ) -> dict:
        """
        Generates content by querying the Gemini API, supporting text and optional image input alongside a specified tool for content generation.

        Args:
            prompt (str): The input text for the content generation query.
            session (Optional[GeminiSession]): A session object for the Gemini API, if None, a new session is created or a default session is used.
            image (Optional[bytes]): Input image bytes for the query; supported image types include JPEG, PNG, and WEBP. This parameter is optional and used for queries that benefit from image context.
            tool (Optional[Tool]): The tool to use for content generation, specifying the context or platform for which the content is relevant. Options include Gmail, Google Docs, Google Drive, Google Flights, Google Hotels, Google Maps, and YouTube. This parameter is optional.

        Returns:
            dict: A dictionary containing the response from the Gemini API, which may include content, conversation ID, response ID, factuality queries, text query, choices, links, images, programming language, code, and status code.
        """
        if self.google_translator_api_key is not None:
            google_official_translator = translate.Client(
                api_key=self.google_translator_api_key
            )

        # [Optional] Language translation
        if (
            self.language is not None
            and self.language not in ALLOWED_LANGUAGES
            and self.google_translator_api_key is None
        ):
            translator_to_eng = GoogleTranslator(source="auto", target="en")
            prompt = translator_to_eng.translate(prompt)
        elif (
            self.language is not None
            and self.language not in ALLOWED_LANGUAGES
            and self.google_translator_api_key is not None
        ):
            prompt = google_official_translator.translate(prompt, target_language="en")
        data = {
            "at": self.token,
            "f.req": json.dumps(
                [None, json.dumps([[prompt], None, session and session.metadata])]
            ),
        }

        # Post request that cannot receive any response due to Google changing the logic for the Gemini API Post to the Web UI.
        try:
            response = self.session.post(
                "https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate",
                data=data,
                timeout=self.timeout,
                proxies=self.proxies,
            )
        except:
            raise TimeoutError(
                "Request timed out. If errors persist, increase the timeout parameter in the Gemini class to a higher number of seconds."
            )
        
        # if response.status_code != 200:
        #     raise APIError(f"Request failed with status code {response.status_code}")
        # else:
        #     try:
        #         body = json.loads(
        #             json.loads(response.text.split("\n")[2])[0][2]
        #         )  # Generated texts
        #         if not body[4]:
        #             body = json.loads(
        #                 json.loads(response.text.split("\n")[2])[4][2]
        #             )  # Non-textual data formats.
        #         if not body[4]:
        #             raise APIError(
        #                 "Failed to parse body. The response body is unstructured. Please try again."
        #             )  # Fail to parse
        #     except Exception:
        #         raise APIError(
        #             "Failed to parse candidates. Unexpected structured response returned. Please try again."
        #         )  # Unexpected structured response

        #     try:
        #         candidates = []
        #         for candidate in body[4]:
        #             web_images = (
        #                 candidate[4]
        #                 and [
        #                     WebImage(
        #                         url=image[0][0][0], title=image[2], alt=image[0][4]
        #                     )
        #                     for image in candidate[4]
        #                 ]
        #                 or []
        #             )
        #             generated_images = (
        #                 candidate[12]
        #                 and candidate[12][7]
        #                 and candidate[12][7][0]
        #                 and [
        #                     GeneratedImage(
        #                         url=image[0][3][3],
        #                         title=f"[Generated image {image[3][6]}]",
        #                         alt=image[3][5][i],
        #                         cookies=self.cookies,
        #                     )
        #                     for i, image in enumerate(candidate[12][7][0])
        #                 ]
        #                 or []
        #             )
        #             candidates.append(
        #                 Candidate(
        #                     rcid=candidate[0],
        #                     text=candidate[1][0],
        #                     web_images=web_images,
        #                     generated_images=generated_images,
        #                 )
        #             )
        #         if not candidates:
        #             raise GeminiError(
        #                 "Failed to generate candidates. No data of any kind returned. If this issue persists, please submit an issue at https://github.com/dsdanielpark/Gemini-API/issues."
        #             )
        #         generated_content = GeminiOutput(
        #             metadata=body[1], candidates=candidates
        #         )
        #     except IndexError:
        #         raise APIError(
        #             "Failed to parse response body. Data structure is invalid. If this issue persists, please submit an issue at https://github.com/dsdanielpark/Gemini-API/issues."
        #         )
        # # Retry to generate content by updating cookies and session
        # if not generated_content:
        #     print(
        #         "Using 'browser_cookie3' package, automatically refresh cookies, re-establish the session, and attempt to generate content again."
        #     )
        #     for _ in range(2):
        #         self.cookies = self._set_cookies(True)
        #         self.session = self._set_session(None)
        #         try:
        #             generated_content = self.generate_content(
        #                 prompt, session, image, tool
        #             )
        #             break
        #         except:
        #             print(
        #                 "Failed to establish session connection after retrying. If this issue persists, please submit an issue at https://github.com/dsdanielpark/Gemini-API/issues."
        #             )
        #     else:
        #         raise APIError("Failed to generate content.")

        # return generated_content
        

    def speech(self, prompt: str, lang: str = "en-US") -> dict:
        """
        Get speech audio from Gemini API for the given input text.

        Args:
            prompt (str): Input text for the query.
            lang (str, optional, default = "en-US"): Input language for the query.

        Returns:
            dict: Answer from the Gemini API in the following format:
            {
                "audio": bytes,
                "status_code": int
            }
        """
        params = {
            "bl": TEXT_GENERATION_WEB_SERVER_PARAM,
            "_reqid": str(self._reqid),
            "rt": "c",
        }

        prompt_struct = [[["XqA3Ic", json.dumps([None, prompt, lang, None, 2])]]]

        data = {
            "f.req": json.dumps(prompt_struct),
            "at": self.token,
        }

        # Get response
        response = self.session.post(
            "https://gemini.google.com/_/BardChatUi/data/batchexecute",
            params=params,
            data=data,
            timeout=self.timeout,
            proxies=self.proxies,
        )

        # Post-processing of response
        response_dict = json.loads(response.content.splitlines()[3])[0][2]
        if not response_dict:
            return {
                "content": f"Response Error: {response.content}. "
                f"\nUnable to get response."
                f"\nPlease double-check the cookie values and verify your network environment or google account."
            }
        resp_json = json.loads(response_dict)
        audio_b64 = resp_json[0]
        audio_bytes = base64.b64decode(audio_b64)
        return {"audio": audio_bytes, "status_code": response.status_code}


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
        gemini: Gemini,
        metadata: Optional[List[str]] = None,
        cid: Optional[str] = None,  # chat id
        rid: Optional[str] = None,  # reply id
        rcid: Optional[str] = None,  # reply candidate id
    ):
        self.__metadata: list[Optional[str]] = [None, None, None]
        self.gemini: Gemini = gemini
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

        if index >= len(self.gemini_output.candidates):
            raise ValueError(
                f"Index {index} exceeds the number of candidates in last model gemini_output."
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
