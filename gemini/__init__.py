# Copyright 2024 Minwoo(Daniel) Park, MIT License
from os import environ
from gemini.core import Gemini
from gemini.constants import (
    HEADERS,
    REPLIT_SUPPORT_PROGRAM_LANGUAGES,
    Tool,
)
from gemini.client import GeminiClient
from gemini.utils import (
    max_token,
    max_sentence,
)

gemini_api_key = environ.get("GEMINI_COOKIES")

__all__ = [
    "GeminiClient",
    "Gemini",
    "max_token",
    "max_sentence",
    "HEADERS",
    "REPLIT_SUPPORT_PROGRAM_LANGUAGES",
    "Tool",
]
__version__ = "0.1.4"
__author__ = "daniel park <parkminwoo1991@gmail.com>"
