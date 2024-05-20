from os import environ

from .client import Gemini
from .async_client import GeminiClient
from .src.modules.openrouter.client import OpenRouter
from .src.modules.openrouter.async_client import AsyncOpenRouter

from .src.model.image import GeminiImage
from .src.model.output import GeminiCandidate, GeminiModelOutput
from .src.model.parser.base import BaesParser
from .src.model.parser.custom_parser import ParseMethod1, ParseMethod2
from .src.model.parser.response_parser import ResponseParser

from .src.misc.constants import URLs, Headers
from .src.misc.decorator import retry, log_method, time_execution, handle_errors
from .src.misc.exceptions import PackageError, GeminiAPIError, TimeoutError
from .src.misc.utils import (
    extract_code,
    upload_image,
    max_token,
    max_sentence,
    load_cookies,
)

from .src.extensions.replit import prepare_replit_data

try:
    from .src.modules.voice.google import google_tts, google_stt
    from .src.modules.voice.openai import openai_tts, openai_stt
except ImportError as e:
    pass


__version__ = "2.4.12"
__author__ = (
    "daniel park <parkminwoo1991@gmail.com>, antonio cheang <teapotv8@proton.me>, "
    "HanaokaYuzu, CBoYXD, veonua, thewh1teagle, jjkoh95, yihong0618, nishantchauhan949, MeemeeLab, kota113, "
    "sachnun, amit9021, zeelsheladiya, ayansengupta17, thecodekitchen, SalimLouDev, Qewertyy, "
    "senseibence, mirusu400, szv99, sudoAlireza"
)
