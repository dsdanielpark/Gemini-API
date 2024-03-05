# Copyright 2024 Daniel Park, Antonio Cheang, MIT License
from os import environ
from .client import GeminiClient
from .core import Gemini
from .src.misc import *
from .src.parser import *
from .src.tools import *
from .src.tools.google import *

gemini_api_key = environ.get("GEMINI_COOKIES")

__version__ = "1.0.4"
__author__ = (
    "daniel park <parkminwoo1991@gmail.com>, antonio cheang <teapotv8@proton.me>"
)
