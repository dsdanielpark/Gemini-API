from os import environ

from .sync_client import Gemini
from .async_client import GeminiClient
from .src.module.openrouter.client import OpenRouter

from .src.model.image import GeminiImage
from .src.model.output import GeminiCandidate, GeminiModelOutput
from .src.model.parser.base import BaesParser
from .src.model.parser.custom_parser import ParseMethod1, ParseMethod2
from .src.model.parser.response_parser import ResponseParser

from .src.misc.constants import URLs, Headers
from .src.misc.decorator import retry, log_method, time_execution, handle_errors
from .src.misc.exceptions import PackageError, GeminiAPIError, TimeoutError
from .src.misc.utils import extract_code, upload_image, max_token, max_sentence

from .src.extension.replit import prepare_replit_data

try:
    from .src.module.voice.google import google_tts, google_stt
    from .src.module.voice.openai import openai_tts, openai_stt
except ImportError as e:
    pass

gemini_api_key = environ.get("GEMINI_COOKIES")

__version__ = "2.4.0"
__author__ = (
    "daniel park <parkminwoo1991@gmail.com>, antonio cheang <teapotv8@proton.me>"
)
