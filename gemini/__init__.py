# Copyright 2024 Minwoo(Daniel) Park, MIT License

from os import environ
from gemini.core import Gemini
from gemini.async_core import BardAsync
from gemini.constants import (
    SESSION_HEADERS,
    ALLOWED_LANGUAGES,
    DEFAULT_LANGUAGE,
    SEPARATOR_LINE,
    USER_PROMPT,
    IMG_UPLOAD_HEADERS,
    Tool,
)
from gemini.utils import (
    extract_links,
    upload_image,
    auto_,
    max_token,
    max_sentence,
)

# Get the API key from the environment variable
bard_api_key = environ.get("_BARD_API_KEY")

__all__ = [
    "Gemini",
    "ChatBard",
    "BardAsync",
    "BardCookies",
    "BardAsyncCookies",
    "SESSION_HEADERS",
    "ALLOWED_LANGUAGES",
    "DEFAULT_LANGUAGE",
    "IMG_UPLOAD_HEADERS",
    "SEPARATOR_LINE",
    "USER_PROMPT",
    "extract_links",
    "upload_image",
    "extract_bard_cookie",
    "max_token",
    "max_sentence",
    "Tool",
]
__version__ = "0.1.0"
__author__ = "daniel park <parkminwoo1991@gmail.com>"
