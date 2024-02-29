# Copyright 2024 Minwoo(Daniel) Park, MIT License
from enum import Enum
from colorama import Fore
import browser_cookie3


class Tool(Enum):
    GMAIL = ["workspace_tool", "Gmail"]
    GOOGLE_DOCS = ["workspace_tool", "Google Docs"]
    GOOGLE_DRIVE = ["workspace_tool", "Google Drive"]
    GOOGLE_FLIGHTS = ["google_flights_tool"]
    GOOGLE_HOTELS = ["google_hotels_tool"]
    GOOGLE_MAPS = ["google_map_tool"]
    YOUTUBE = ["youtube_tool"]


DEFAULT_LANGUAGE = "en"
SEPARATOR_LINE = "=" * 36
USER_PROMPT = Fore.BLUE + "You: " + Fore.RESET
TEXT_GENERATION_WEB_SERVER_PARAM = "boq_assistant-bard-web-server_20240222.09_p2"
POST_ENDPOINT = "https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate"
HOST = "https://gemini.google.com"
SHARE_ENDPOINT = "https://clients6.google.com/upload/drive/v3/"
BOT_SERVER = "boq_assistant-bard-web-server_20240227.13_p0"


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
    "Origin": "https://gemini.google.com",
    "DNT": "1",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
}

IMG_UPLOAD_HEADERS = {
    "authority": "content-push.googleapis.com",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.7",
    "authorization": "Basic c2F2ZXM6cyNMdGhlNmxzd2F2b0RsN3J1d1U=",  # Constant Authorization Key
    "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    "origin": "https://gemini.google.com",
    "push-id": "feeds/mcudyrk2a4khkz",  # Constant
    "referer": "https://gemini.google.com/",
    "x-goog-upload-command": "start",
    "x-goog-upload-header-content-length": "",
    "x-goog-upload-protocol": "resumable",
    "x-tenant-id": "bard-storage",
}

REPLIT_SUPPORT_PROGRAM_LANGUAGES = {
    "python": "main.py",
    "javascript": "index.js",
    "go": "main.go",
    "java": "Main.java",
    "kotlin": "Main.kt",
    "php": "index.php",
    "c#": "main.cs",
    "swift": "main.swift",
    "r": "main.r",
    "ruby": "main.rb",
    "c": "main.c",
    "c++": "main.cpp",
    "matlab": "main.m",
    "typescript": "main.ts",
    "scala": "main.scala",
    "sql": "main.sql",
    "html": "index.html",
    "css": "style.css",
    "nosql": "main.nosql",
    "rust": "main.rs",
    "perl": "main.pl",
}


SUPPORTED_BROWSERS = [
    browser_cookie3.chrome,
    browser_cookie3.chromium,
    browser_cookie3.opera,
    browser_cookie3.opera_gx,
    browser_cookie3.brave,
    browser_cookie3.edge,
    browser_cookie3.vivaldi,
    browser_cookie3.firefox,
    browser_cookie3.librewolf,
    browser_cookie3.safari,
]
