print("Starting")

import os
import sys
import json
import requests
import subprocess
import whisper
import warnings
import asyncio
import re
import speech_recognition as sr
import platform
import webbrowser
import urllib.parse
import speech_recognition as sr
from tkinter import Tk, Text, Button
from gtts import gTTS
import threading
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import speech_recognition as sr
import pyaudio
from pydub import AudioSegment
from pydub import playback
from pydub.playback import play
from playsound import playsound
from Bard import Chatbot
from google_images_download import google_images_download
from google_images_search import GoogleImagesSearch
from flask import Flask, request, redirect

print("L Done")

#Google
r = sr.Recognizer()
token = 'YwhXxoHIAg68RXgIOt2PoFtNQe944EI-ug3weQGUZXLmI_UyPzHeCPXyowhxRonyWlugfg.'
chatbot = Chatbot(token)
small_model = whisper.load_model('small')
base_model = whisper.load_model('base')

if sys.platform != 'darwin':
    import pyttsx3
    engine = pyttsx3.init() 
    # Get the current speech rate
    rate = engine.getProperty('rate')
    # Decrease speech rate by 50 words per minute (Change as desired)
    engine.setProperty('rate', rate-50)

def prompt_bard(prompt):
    response = chatbot.ask(prompt)
    return response['content']
print("G Done")

def speak(text):
    # If Mac OS use system messages for TTS
    if sys.platform == 'darwin':
        ALLOWED_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,?!-_$: ")
        clean_text = ''.join(c for c in text if c in ALLOWED_CHARS)
        system(f"say '{clean_text}'")
    # Use pyttsx3 for other operating sytstems
    else:
        engine.say(text)
        engine.runAndWait()

# Spotify API credentials
client_id = 'a1004960c590470db66ffef7e4e260d4'
client_secret = 'cf3e9a286bc245d2b015e755663adda8'
redirect_uri = 'http://localhost:5420/callback'
username = 'euqf7m7eo8hgdyqc5pmlcw8fz'
scope = 'user-modify-playback-state'
access_token = ''
sp = None  # Define sp globally

# Function to obtain an access token from Spotify
def get_access_token():
    sp_oauth = spotipy.oauth2.SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        cache_path=".spotifycache",
        show_dialog=True
    )
    auth_url = sp_oauth.get_authorize_url()
    print(f"Please visit this URL to authorize your application: {auth_url}")
    auth_response = input("Enter the URL you were redirected to: ")
    code = sp_oauth.parse_response_code(auth_response)
    sp_oauth.get_access_token(code)
    return spotipy.Spotify(auth_manager=sp_oauth)

# Call the function to retrieve the access token and assign the returned value to the global sp object
sp = get_access_token()

# Function to play Spotify
def play_spotify():
    sp.start_playback()

# Function to pause Spotify
def pause_spotify():
    sp.pause_playback()

# Function to skip to the next track on Spotify
def skip_spotify():
    sp.next_track()

# Function to rewind to the previous track on Spotify
def rewind_spotify():
    sp.previous_track()
     
# Function to open Spotify
def open_spotify():
    current_platform = platform.system()
    if current_platform == 'Darwin':  # macOS
        subprocess.call(['open', '-a', 'Spotify'])
    elif current_platform == 'Windows':
        subprocess.call(['start', 'spotify'])
    else:
        print("Unsupported platform.")

print("S Done")

def main():
    # Initialize microphone object
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        # Runs program indefinitely
        while True:
            # Continuously listens for wake word locally
            while True:
                try:
                    print("Clear")
                    audio = r.listen(source)
                    with open("detect.wav", "wb") as f:
                        f.write(audio.get_wav_data())
                    # Transcribe wake word using whisper tiny model
                    result = small_model.transcribe('detect.wav')
                    text_input = result['text']
                    # If wake word is found, break out of loop
                    if 'elora' in text_input.lower().strip():
                        text_input.replace("elora", "google")
                        break
                    else:
                        print("Try again.")
                except Exception as e:
                    print("Error transcribing audio: ", e)
                    continue
            try:
                # Play wake word detected notification sound 
                playsound('wake_detected.mp3')
                print("Detected. Please speak your prompt. \n")
                # Record prompt
                audio = r.listen(source)
                with open("prompt.wav", "wb") as f:
                    f.write(audio.get_wav_data())
                # Transcribe prompt using whisper base model
                result = base_model.transcribe('prompt.wav')
                prompt_text = result['text']
                print("Sending to Bard:", prompt_text, '\n')
                # If prompt is empty, start listening for wake word again
                if len(prompt_text.strip()) == 0:
                    print("Empty")
                    speak("Empty")
                    continue
            except Exception as e:
                print("Error transcribing audio: ", e)
                continue
            # Prompt Bard. 
            response = prompt_bard(prompt_text)
            # Prints Bard response normal if windows (cannot ASCII delete in command prompt to change font color)
            if sys.platform.startswith('win'):
                 print('Bards response: ', response)
            else:
                # Prints Bard response in red for linux & mac terminal
                print("\033[31m" + 'Bards response: ', response, '\n' + "\033[0m")
            speak(response)

# Function to play audio using pydub
#def play_audio(audio):
    audio.export("output.wav", format="wav")
    audio = AudioSegment.from_wav("output.wav")
    play(audio)
print("A Done")

# Function to search the web
def search_web(query):
    query = urllib.parse.quote_plus(query)  # URL-encode the search query
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

# Function to search images
def search_images(query):
    response = google_images_download.googleimagesdownload()

    # Configure the search parameters
    search_params = {
        'keywords': query,
        'limit': 5,  # Number of images to retrieve
        'safe_search': True,  # Safe search filter
        'format': 'jpg',  # Limit search to JPEG format
        'output_directory': 'images'  # Directory to save the images
    }

    # Perform the search
    response.download(search_params)

    # Get the paths of the downloaded images
    image_paths = response.paths

    # Open the first image in a web browser
    if image_paths:
        image_path = image_paths[0]
        webbrowser.open(image_path)

# Function to set up the image search client
def setup_image_search_client(api_key, cx):
    gis = GoogleImagesSearch(api_key, cx)
    return gis
print("I Done")

# Function to run the Elora interactive window
def run_elora():
    # Create a new Tkinter window
    window = Tk()

    # Define the properties of the window
    window.title("E.L.O.R.A")
    window.geometry("400x300")

    # Create a text widget to display the recognized speech
    speech_text = Text(window, height=20, width=50)
    speech_text.pack()

    # Start updating the speech text
    speech_text.after(1000, update_speech_text, speech_text)

    # Start the main loop of the GUI
    window.mainloop()

def update_speech_text(speech_text):
    def update_text():
        command = asyncio.run(main())
        speech_text.delete("1.0", "end")
        speech_text.insert("end", command)
        speech_text.after(1000, update_speech_text, speech_text)
    threading.Thread(target=update_text).start()
print("W Done")

# Create the Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, world!'  # Replace with your desired response

# Callback route for Spotify authentication
@app.route('/callback')
def callback():
    global sp
    # Retrieve the authorization code
    code = request.args.get('code')

    # Use the authorization code to obtain an access token
    sp_oauth = spotipy.oauth2.SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        cache_path=".spotifycache",
        show_dialog=True
    )
    token_info = sp_oauth.get_access_token(code, as_dict=False)
    access_token = token_info['access_token'][0]
    sp = spotipy.Spotify(auth=access_token)
    
    return 'Authentication successful! You can close this window.'

# Add the routes before starting the app
app.add_url_rule('/', 'home', home)
print("O Done")

app.run(port=5420)
print("Port Done")

if __name__ == '__main__':
    main()
    print("M Done")