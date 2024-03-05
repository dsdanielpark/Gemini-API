# Copyright 2024 Daniel Park, Antonio Cheang, MIT License
import json
import requests
from .constants import IMG_UPLOAD_HEADERS, REPLIT_SUPPORT_PROGRAM_LANGUAGES


def extract_code(text: str, language: str) -> str:
    """
    Extracts code snippets for the specified programming language from the given text.
    If only one snippet is found, returns it directly instead of a list.
    If no snippets are found, returns the original text.

    Args:
        text (str): The text containing mixed code snippets.
        language (str): The programming language of the code snippets to extract.

    Returns:
        str or list of str: A single code snippet string if only one is found, otherwise a list of all extracted code snippets for the specified language. Returns the original text if no snippets are found.

    Raises:
        ValueError: If the specified language is not supported.
    """
    language = language.lower()
    if language not in REPLIT_SUPPORT_PROGRAM_LANGUAGES:
        supported_languages = ", ".join(REPLIT_SUPPORT_PROGRAM_LANGUAGES.keys())
        raise ValueError(
            f"Unsupported language. Please choose from the following: {supported_languages}"
        )

    snippets = []
    start_pattern = f"```{language}"
    end_pattern = "```"
    start_idx = text.find(start_pattern)

    while start_idx != -1:
        end_idx = text.find(end_pattern, start_idx + len(start_pattern))
        if end_idx != -1:
            snippet = text[start_idx + len(start_pattern) : end_idx].strip()
            snippets.append(snippet)
            start_idx = text.find(start_pattern, end_idx + len(end_pattern))
        else:
            break

    # Return directly if only one snippet is found
    if len(snippets) == 1:
        return snippets[0]
    elif len(snippets) > 1:
        return snippets
    else:
        # Return the original text if no snippets are found
        return text


def upload_image(image: bytes, filename: str = "Photo.jpg"):
    """
    Upload image into bard bucket on Google API, do not need session.

    Returns:
        str: relative URL of image.
    """
    resp = requests.options("https://content-push.googleapis.com/upload/")
    resp.raise_for_status()
    size = len(image)

    headers = IMG_UPLOAD_HEADERS
    headers["size"] = str(size)
    headers["x-goog-upload-command"] = "start"

    data = f"File name: {filename}"
    resp = requests.post(
        "https://content-push.googleapis.com/upload/", headers=headers, data=data
    )
    resp.raise_for_status()
    upload_url = resp.headers["X-Goog-Upload-Url"]
    resp = requests.options(upload_url, headers=headers)
    resp.raise_for_status()
    headers["x-goog-upload-command"] = "upload, finalize"

    # It can be that we need to check returned offset
    headers["X-Goog-Upload-Offset"] = "0"
    resp = requests.post(upload_url, headers=headers, data=image)
    resp.raise_for_status()
    return resp.text


def max_token(text: str, n: int) -> str:
    """
    Return the first 'n' tokens (words) of the given text.

    Args:
        text (str): The input text to be processed.
        n (int): The number of tokens (words) to be included in the result.

    Returns:
        str: The first 'n' tokens from the input text.
    """
    if not isinstance(text, str):
        raise ValueError("Input 'text' must be a valid string.")

    tokens = text.split()  # Split the text into tokens (words)
    if n <= len(tokens):
        return " ".join(tokens[:n])  # Return the first 'n' tokens as a string
    else:
        return text


def max_sentence(text: str, n: int):
    """
    Print the first 'n' sentences of the given text.

    Args:
        text (str): The input text to be processed.
        n (int): The number of sentences to be printed from the beginning.

    Returns:
        None
    """
    punctuations = set("?!.")

    sentences = []
    sentence_count = 0
    for char in text:
        sentences.append(char)
        if char in punctuations:
            sentence_count += 1
            if sentence_count == n:
                result = "".join(sentences).strip()
                return result


def build_replit_data(instructions: str, code: str, filename: str) -> list:
    """
    Creates and returns the input_image_data_struct based on provided parameters.

    :param instructions: The instruction text.
    :param code: The code.
    :param filename: The filename.

    :return: The input_image_data_struct.
    """
    return [
        [
            [
                "qACoKe",
                json.dumps([instructions, 5, code, [[filename, code]]]),
                None,
                "generic",
            ]
        ]
    ]
