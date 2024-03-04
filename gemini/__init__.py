# Copyright 2024 Daniel Park, Antonio Cheang, MIT License
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
__version__ = "1.0.2"
__author__ = (
    "daniel park <parkminwoo1991@gmail.com>, antonio cheang <teapotv8@proton.me>"
)
