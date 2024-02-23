# Copyright 2024 Minwoo(Daniel) Park, MIT License
import base64
import json
import os
import random
import re
import string
import uuid
import requests
from typing import Optional

try:
    from langdetect import detect
    from deep_translator import GoogleTranslator
    from google.cloud import translate_v2 as translate
except ImportError:
    pass
from .constants import (
    ALLOWED_LANGUAGES,
    REPLIT_SUPPORT_PROGRAM_LANGUAGES,
    SESSION_HEADERS,
    TEXT_GENERATION_WEB_SERVER_PARAM,
    Tool,
)
from .utils import (
    build_export_data_structure,
    build_input_replit_data_struct,
    extract_cookies_from_brwoser,
    upload_image,
)
from .models.base import (
    GeminiOutput,
    Candidate,
    WebImage,
    GeneratedImage,
)
from .models.exceptions import (
    APIError,
    GeminiError,
    TimeoutError,
)
from .models.session import GeminiSession


class Gemini:
    """
    Gemini class for interacting with Google Gemini service.
    """

    __slots__ = [
        "session",
        "cookies",
        "timeout",
        "proxies",
        "language",
        "conversation_id",
        "auto_cookies",
        "google_translator_api_key",
        "run_code",
    ]

    def __init__(
        self,
        session: Optional[requests.Session] = None,
        cookies: dict = None,
        timeout: int = 20,
        proxies: Optional[dict] = None,
        language: Optional[str] = None,
        conversation_id: Optional[str] = None,
        google_translator_api_key: Optional[str] = None,
        run_code: bool = False,
        auto_cookies: bool = False,
    ):
        """
        Initialize the Gemini instance.

        Args:
            cookies (dict, optional): Pass 3 cookies (__Secure-1PSID, __Secure-1PSIDTS, __Secure-1PSIDCC) as keys with their respective values.
            timeout (int, optional, default = 20): Request timeout in seconds.
            proxies (dict, optional): Proxy configuration for requests.
            session (requests.Session, optional): Requests session object.
            conversation_id (str, optional): ID for fetching conversational context.
            google_translator_api_key (str, optional): Google Cloud Translation API key.
            language (str, optional): Natural language code for translation (e.g., "en", "ko", "ja").
            run_code (bool, optional, default = False): Whether to directly execute the code included in the answer (IPython only).
            auto_cookies (bool, optional, default = False): Retrieve a token from the browser.
        """
        self.cookies = cookies or self._get_auto_cookies(auto_cookies)
        self.session = self._get_session(session)
        self.proxies = proxies
        self.timeout = timeout
        self.SNlM0e = self._get_snim0e()
        self.language = language or os.getenv("GEMINI_LANGUAGE")
        self.run_code = run_code
        self.google_translator_api_key = google_translator_api_key
        self._reqid = int("".join(random.choices(string.digits, k=4)))
        self.conversation_id = conversation_id or ""
        self.response_id = ""
        self.choice_id = ""
        self.og_pid = ""
        self.rot = ""
        self.exp_id = ""
        self.init_value = ""

    def _get_auto_cookies(self, auto_cookies: bool) -> dict:
        """
        Get the Gemini API token either from the provided token or from the browser cookie.

        Args:
            auto_cookies (bool): Whether to extract the token from the browser cookie.

        Returns:
            dict: The dictionary containing the extracted cookies.

        Raises:
            Exception: If the token is not provided and can't be extracted from the browser.
        """
        env_cookies = os.getenv("GEMINI_COOKIES_DICT")
        if env_cookies:
            return env_cookies

        if auto_cookies:
            extracted_cookie_dict = extract_cookies_from_brwoser()
            self.cookies = extracted_cookie_dict
            if extracted_cookie_dict:
                return extracted_cookie_dict

        raise Exception(
            "Gemini cookies must be provided as the 'cookies' argument or extracted from the browser."
        )

    def _get_session(self, session: Optional[requests.Session]) -> requests.Session:
        """
        Get the requests Session object.

        Args:
            session (requests.Session): Requests session object.

        Returns:
            requests.Session: The Session object.
        """
        if session is not None:
            return session

        session = requests.Session()
        session.headers = SESSION_HEADERS
        session.cookies.set("__Secure-1PSID", self.cookies["__Secure-1PSID"])
        session.proxies = self.proxies

        if self.cookies is not None:
            for k, v in self.cookies.items():
                session.cookies.set(k, v)

        return session

    def _get_snim0e(self) -> str:
        """
        Get the SNlM0e value from the Gemini API response.

        Returns:
            str: SNlM0e value.
        Raises:
            Exception: If the __Secure-1PSID value is invalid or SNlM0e value is not found in the response.
        """
        response = self.session.get(
            "https://gemini.google.com/app", timeout=self.timeout, proxies=self.proxies
        )
        if response.status_code != 200:
            raise Exception(
                f"Response status code is not 200. Response Status is {response.status_code}"
            )
        snim0e = re.search(r"SNlM0e\":\"(.*?)\"", response.text)
        if not snim0e:
            raise Exception(
                "SNlM0e value not found. Double-check cookies dict value or pass it as Gemini(cookies=Dict())"
            )
        return snim0e.group(1)

    def generate_content(
        self,
        prompt: str,
        session: Optional["GeminiSession"] = None,
        image: Optional[bytes] = None,
        tool: Optional[Tool] = None,
    ) -> dict:
        """
        Get an answer from the Gemini API for the given input text.

        Example:
        >>> cookies = Dict()
        >>> Gemini = Gemini(cookies=cookies)
        >>> response = Gemini.get_answer("나와 내 동년배들이 좋아하는 뉴진스에 대해서 알려줘")
        >>> print(response['content'])

        Args:
            prompt (str): Input text for the query.
            image (bytes): Input image bytes for the query, support image types: jpeg, png, webp
            image_name (str): Short file name
            tool : tool to use can be one of Gmail, Google Docs, Google Drive, Google Flights, Google Hotels, Google Maps, Youtube

        Returns:
            dict: Answer from the Gemini API in the following format:
                {
                    "content": str,
                    "conversation_id": str,
                    "response_id": str,
                    "factuality_queries": list,
                    "text_query": str,
                    "choices": list,
                    "links": list,
                    "images": list,
                    "program_lang": str,
                    "code": str,
                    "status_code": int
                }
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
            "at": self.SNlM0e,
            "f.req": json.dumps(
                [None, json.dumps([[prompt], None, session and session.metadata])]
            ),
        }
        # Get response
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

        if response.status_code != 200:
            raise APIError(f"Request failed with status code {response.status_code}")
        else:
            try:
                body = json.loads(
                    json.loads(response.text.split("\n")[2])[0][2]
                )  # Generated texts
                if not body[4]:
                    body = json.loads(
                        json.loads(response.text.split("\n")[2])[4][2]
                    )  # Non-textual data formats.
                if not body[4]:
                    raise APIError(
                        "Failed to parse body. The response body is unstructured. Please try again."
                    )  # Fail to parse
            except Exception:
                raise APIError(
                    "Failed to parse candidates. Unexpected structured response returned. Please try again."
                )  # Unexpected structured

            try:
                candidates = []
                for candidate in body[4]:
                    web_images = (
                        candidate[4]
                        and [
                            WebImage(
                                url=image[0][0][0], title=image[2], alt=image[0][4]
                            )
                            for image in candidate[4]
                        ]
                        or []
                    )
                    generated_images = (
                        candidate[12]
                        and candidate[12][7]
                        and candidate[12][7][0]
                        and [
                            GeneratedImage(
                                url=image[0][3][3],
                                title=f"[Generated image {image[3][6]}]",
                                alt=image[3][5][i],
                                cookies=self.cookies,
                            )
                            for i, image in enumerate(candidate[12][7][0])
                        ]
                        or []
                    )
                    candidates.append(
                        Candidate(
                            rcid=candidate[0],
                            text=candidate[1][0],
                            web_images=web_images,
                            generated_images=generated_images,
                        )
                    )
                if not candidates:
                    raise GeminiError(
                        "Failed to generate candidates. No data of any kind returned."
                    )
                generated_content = GeminiOutput(
                    metadata=body[1], candidates=candidates
                )
            except IndexError:
                raise APIError(
                    "Failed to parse response body. Data structure is invalid."
                )
        return generated_content

    def speech(self, prompt: str, lang: str = "en-US") -> dict:
        """
        Get speech audio from Gemini API for the given input text.

        Example:
        >>> cookies = Dict()
        >>> Gemini = Gemini(cookies=cookies)
        >>> audio = Gemini.speech("Say hello!")
        >>> with open("Gemini.ogg", "wb") as f:
        >>>     f.write(bytes(audio['audio']))

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
            "at": self.SNlM0e,
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

    def export_conversation(self, generated_content, title: str = "") -> dict:
        """
        Get Share URL for specific answer from Gemini

        Example:
        >>> cookies = Dict()
        >>> Gemini = Gemini(cookies = cookies)
        >>> generated_content = Gemini.get_answer("hello!")
        >>> url = Gemini.export_conversation(generated_content, title="Export Conversation")
        >>> print(url['url'])

        Args:
            generated_content (dict): generated_content returned from get_answer
            title (str, optional, default = ""): Title for URL
        Returns:
            dict: Answer from the Gemini API in the following format:
            {
                "url": str,
                "status_code": int
            }
        """
        conv_id = generated_content["conversation_id"]
        resp_id = generated_content["response_id"]
        choice_id = generated_content["choices"][0]["id"]
        params = {
            "rpcids": "fuVx7",
            "source-path": "/",
            "bl": TEXT_GENERATION_WEB_SERVER_PARAM,
            "rt": "c",
        }

        # Build data structure
        export_data_structure = build_export_data_structure(
            conv_id, resp_id, choice_id, title
        )

        data = {
            "f.req": json.dumps(export_data_structure),
            "at": self.SNlM0e,
        }
        response = self.session.post(
            "https://gemini.google.com/_/BardChatUi/data/batchexecute",
            params=params,
            data=data,
            timeout=self.timeout,
            proxies=self.proxies,
        )

        # Post-processing of response
        response_dict = json.loads(response.content.splitlines()[3])
        url_id = json.loads(response_dict[0][2])[2]
        url = f"https://g.co/Gemini/share/{url_id}"

        # Increment request ID
        self._reqid += 100000
        return {"url": url, "status_code": response.status_code}

    def ask_about_image(
        self, prompt: str, image: bytes, lang: Optional[str] = None
    ) -> dict:
        """
        Send Gemini image along with question and get answer

        Example:
        >>> cookies = Dict()
        >>> Gemini = Gemini(cookies = cookies)
        >>> image = open('image.jpg', 'rb').read()
        >>> generated_content = Gemini.ask_about_image("what is in the image?", image)['content']

        Args:
            prompt (str): Input text for the query.
            image (bytes): Input image bytes for the query, support image types: jpeg, png, webp
            lang (str, optional): Language to use.

        Returns:
            dict: Answer from the Gemini API in the following format:
                {
                    "content": str,
                    "conversation_id": str,
                    "response_id": str,
                    "factuality_queries": list,
                    "text_query": str,
                    "choices": list,
                    "links": list,
                    "images": list,
                    "program_lang": str,
                    "code": str,
                    "status_code": int
                }
        """
        if self.google_translator_api_key is not None:
            google_official_translator = translate.Client(
                api_key=self.google_translator_api_key
            )
        elif self.language is not None or lang is not None:
            translator_to_eng = GoogleTranslator(source="auto", target="en")

        # [Optional] Set language
        if self.language is None and lang is None:
            translated_prompt = prompt
        elif (
            (self.language is not None or lang is not None)
            and self.language not in ALLOWED_LANGUAGES
            and self.google_translator_api_key is None
        ):
            translator_to_eng = GoogleTranslator(source="auto", target="en")
            translated_prompt = translator_to_eng.translate(prompt)
        elif (
            (self.language is not None or lang is not None)
            and self.language not in ALLOWED_LANGUAGES
            and self.google_translator_api_key is not None
        ):
            translated_prompt = google_official_translator.translate(
                prompt, target_language="en"
            )
        elif (
            (self.language is None or lang is None)
            and self.language not in ALLOWED_LANGUAGES
            and self.google_translator_api_key is None
        ):
            translator_to_eng = GoogleTranslator(source="auto", target="en")
            translated_prompt = translator_to_eng.translate(prompt)

        # Supported format: jpeg, png, webp
        image_url = upload_image(image)

        input_data_struct = [
            None,
            [
                [
                    translated_prompt,
                    0,
                    None,
                    [[[image_url, 1], "uploaded_photo.jpg"]],
                ],
                [lang if lang is not None else self.language],
                ["", "", ""],
                "",  # Unknown random string value (1000 characters +)
                uuid.uuid4().hex,  # Should be random uuidv4 (32 characters)
                None,
                [1],
                0,
                [],
                [],
            ],
        ]
        params = {
            "bl": "boq_assistant-Gemini-web-server_20230716.16_p2",
            "_reqid": str(self._reqid),
            "rt": "c",
        }
        input_data_struct[1] = json.dumps(input_data_struct[1])
        data = {
            "f.req": json.dumps(input_data_struct),
            "at": self.SNlM0e,
        }

        response = self.session.post(
            "https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate",
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
        parsed_answer = json.loads(response_dict)
        content = parsed_answer[4][0][1][0]
        try:
            if self.language is None and self.google_translator_api_key is None:
                translated_content = content
            elif self.language is not None and self.google_translator_api_key is None:
                translator = GoogleTranslator(source="en", target=self.language)
                translated_content = translator.translate(content)

            elif lang is not None and self.google_translator_api_key is None:
                translator = GoogleTranslator(source="en", target=lang)
                translated_content = translator.translate(content)

            elif (
                lang is None and self.language is None
            ) and self.google_translator_api_key is None:
                us_lang = detect(prompt)
                translator = GoogleTranslator(source="en", target=us_lang)
                translated_content = translator.translate(content)

            elif (
                self.language is not None and self.google_translator_api_key is not None
            ):
                translated_content = google_official_translator.translate(
                    content, target_language=self.language
                )
            elif lang is not None and self.google_translator_api_key is not None:
                translated_content = google_official_translator.translate(
                    content, target_language=lang
                )
            elif (
                self.language is None and lang is None
            ) and self.google_translator_api_key is not None:
                us_lang = detect(prompt)
                translated_content = google_official_translator.translate(
                    content, target_language=us_lang
                )
        except Exception as e:
            print(f"Translation failed, and the original text has been returned. \n{e}")
            translated_content = content

        # Returned dictionary object
        generated_content = {
            "content": translated_content,
            "conversation_id": parsed_answer[1][0],
            "response_id": parsed_answer[1][1],
            "factuality_queries": parsed_answer[3],
            "text_query": parsed_answer[2][0] if parsed_answer[2] else "",
            "choices": [{"id": x[0], "content": x[1]} for x in parsed_answer[4]],
            "links": self._extract_links(parsed_answer[4]),
            "images": [""],
            "program_lang": "",
            "code": "",
            "status_code": response.status_code,
        }
        self.conversation_id, self.response_id, self.choice_id = (
            generated_content["conversation_id"],
            generated_content["response_id"],
            generated_content["choices"][0]["id"],
        )
        self._reqid += 100000
        return generated_content

    def export_replit(
        self,
        code: str,
        program_lang: Optional[str] = None,
        filename: Optional[str] = None,
        **kwargs,
    ) -> dict:
        """
        Get export URL to repl.it from code

        Example:
        >>> cookies = Dict()
        >>> Gemini = Gemini(cookies = cookies)
        >>> generated_content = Gemini.get_answer("Give me python code to print hello world")
        >>> url = Gemini.export_replit(generated_content['code'], generated_content['program_lang'])
        >>> print(url['url'])

        Args:
            code (str): source code
            program_lang (str, optional): programming language
            filename (str, optional): filename
            **kwargs: instructions, source_path
        Returns:
        dict: Answer from the Gemini API in the following format:
            {
                "url": str,
                "status_code": int
            }
        """
        params = {
            "rpcids": "qACoKe",
            "source-path": kwargs.get("source_path", "/"),
            "bl": TEXT_GENERATION_WEB_SERVER_PARAM,
            "_reqid": str(self._reqid),
            "rt": "c",
        }

        # Reference: https://github.com/jincheng9/markdown_supported_languages
        if program_lang not in REPLIT_SUPPORT_PROGRAM_LANGUAGES and filename is None:
            raise Exception(
                f"Language {program_lang} not supported, please set filename manually."
            )

        filename = (
            REPLIT_SUPPORT_PROGRAM_LANGUAGES.get(program_lang, filename)
            if filename is None
            else filename
        )
        input_replit_data_struct = build_input_replit_data_struct(
            kwargs.get("instructions", ""), code, filename
        )

        data = {
            "f.req": json.dumps(input_replit_data_struct),
            "at": self.SNlM0e,
        }

        # Get response
        response = self.session.post(
            "https://gemini.google.com/_/BardChatUi/data/batchexecute",
            params=params,
            data=data,
            timeout=self.timeout,
            proxies=self.proxies,
        )

        response_dict = json.loads(response.content.splitlines()[3])
        print(f"Response: {response_dict}")

        url = json.loads(response_dict[0][2])[0]

        # Increment request ID
        self._reqid += 100000

        return {"url": url, "status_code": response.status_code}

    def _extract_links(self, data: list) -> list:
        """
        Extract links from the given data.

        Args:
            data: Data to extract links from.

        Returns:
            list: Extracted links.
        """
        links = []
        if isinstance(data, list):
            for item in data:
                if isinstance(item, list):
                    links.extend(self._extract_links(item))
                elif (
                    isinstance(item, str)
                    and item.startswith("http")
                    and "favicon" not in item
                ):
                    links.append(item)
        return links
