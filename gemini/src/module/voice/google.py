# To-Do: Need QA and error handling
import os
from gtts import gTTS
import speech_recognition as sr


def google_tts(text, cache_dir, lang="en"):
    """
    Generates and saves a spoken version of the input text using Google's Text-to-Speech API.

    Parameters:
    - text (str): The text to be converted to speech.
    - cache_dir (str): Directory where the speech file will be saved.
    - lang (str): The language of the text (default is English, 'en').

    Returns:
    - str: The file path of the saved speech file.

    Example:
    >>> save_path = google_tts("Hello, world!", "./cache", "en")
    >>> print(save_path)
    ./cache/tts.mp3
    """
    tts = gTTS(text=text, lang=lang)
    os.makedirs(cache_dir, exist_ok=True)
    save_path = f"{cache_dir}/tts.mp3"
    tts.save(save_path)
    return save_path


def google_stt(audio_file_path: str, recognizer: str = "google") -> str:
    """
    Converts speech in an audio file to text using various Speech Recognition APIs.

    Args:
        audio_file_path (str): The file path of the audio file to be transcribed.
        recognizer (str): The speech recognition service to use. Options include 'google', 'bing', 'google_cloud',
                          'houndify', 'ibm', 'sphinx', 'wit'. Default is 'google'.

    Returns:
        str: The text transcription of the audio file. Returns an error message if conversion fails or file format is incompatible.

    Raises:
        ValueError: If the audio file format is not supported or recognizer is not recognized.

    Example:
        >>> text = speech_to_text("./cache/audio.wav", recognizer='google')
        >>> print(text)
        'Hello, world!'
    """
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio_text = r.listen(source)
    except (EOFError, ValueError) as e:
        return f"Error processing audio file: {e}. Ensure file is a compatible format (WAV, AIFF, FLAC)."

    try:
        text = {
            "google": lambda audio: r.recognize_google(audio),
            # Add other recognizers here following the pattern
        }.get(recognizer, lambda audio: None)(audio_text)

        if text is None:
            raise ValueError(f"Recognizer '{recognizer}' is not supported.")

        return text
    except Exception as e:
        return f"Failed to convert speech to text: {e}."
