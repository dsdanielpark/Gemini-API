# Copyright 2024 Minwoo(Daniel) Park, MIT License
from os import environ
from gemini.core import Gemini, GeminiSession
from gemini.constants import (
    SESSION_HEADERS,
    ALLOWED_LANGUAGES,
    DEFAULT_LANGUAGE,
    REPLIT_SUPPORT_PROGRAM_LANGUAGES,
    REQUIRED_COOKIE_LIST,
    Tool,
)
from gemini.utils import (
    extract_links,
    upload_image,
    extract_cookies_from_brwoser,
    max_token,
    max_sentence,
)

gemini_api_key = environ.get("GEMINI_COOKIES")

__all__ = [
    "Gemini",
    "GeminiSession",
    "extract_links",
    "upload_image",
    "extract_cookies_from_brwoser",
    "max_token",
    "max_sentence",
    "DEFAULT_LANGUAGE",
    "SESSION_HEADERS",
    "ALLOWED_LANGUAGES",
    "REPLIT_SUPPORT_PROGRAM_LANGUAGES",
    "REQUIRED_COOKIE_LIST",
    "Tool",
]
__version__ = "0.1.0"
__author__ = "daniel park <parkminwoo1991@gmail.com>"
