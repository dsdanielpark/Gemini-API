# To-Do: Need QA and error handling
from pathlib import Path
from openai import OpenAI


def openai_tts(
    text_input,
    output_file_name=None,
    model="tts-1",
    voice="alloy",
    stream_to_file=False,
):
    """
    Converts text to speech using OpenAI's API. Depending on the parameters, it can save the output to a file or return the audio content.

    Parameters:
    - text_input (str): The text to be converted to speech.
    - output_file_name (str, optional): The name of the output file where the speech audio will be saved if stream_to_file is True. Defaults to None.
    - model (str, optional): The model to use for text-to-speech conversion. Defaults to "tts-1".
    - voice (str, optional): The voice model to use. Defaults to "alloy".
    - stream_to_file (bool, optional): Whether to stream the output directly to a file. If False, returns the audio content. Defaults to True.

    Example:
    ```
    # Example usage to save output to a file
    text_input = "Hello world! This is a streaming test."
    output_file_name = "output.mp3"
    openai_tts(text_input, output_file_name=output_file_name, stream_to_file=False)

    # Example usage to get audio content without saving to a file
    audio_content = openai_tts(text_input, stream_to_file=False)
    ```
    """
    client = OpenAI()
    response = client.audio.speech.create(model=model, voice=voice, input=text_input)

    if stream_to_file and output_file_name:
        # Determine the full path for the output file
        speech_file_path = Path(__file__).parent / output_file_name
        response.stream_to_file(speech_file_path)
        print(f"Audio file saved to: {speech_file_path}")
    else:
        # Return the audio content directly
        return response.content


def openai_stt(audio_file_path, model="whisper-1", response_format="text"):
    """
    Converts speech to text using OpenAI's API. This function opens an audio file, sends it for transcription, and either prints or returns the transcribed text.

    Parameters:
    - audio_file_path (str): The path to the audio file to be transcribed.
    - model (str, optional): The model to use for speech-to-text conversion. Defaults to "whisper-1".
    - response_format (str, optional): The format of the response. Defaults to "text".

    Returns:
    The transcribed text as a string if response_format is "text".

    Example:
    ```
    # Example usage to print transcription
    audio_file_path = "/path/to/file/audio.mp3"
    transcribed_text = openai_stt(audio_file_path)
    print(transcribed_text)

    # Example usage with a different model and response format
    audio_file_path = "/path/to/file/speech.mp3"
    transcribed_text = openai_stt(audio_file_path, model="whisper-1", response_format="text")
    print(transcribed_text)
    ```
    """
    client = OpenAI()
    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=model, file=audio_file, response_format=response_format
        )
    return transcription.text
