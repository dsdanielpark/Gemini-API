Development Status :: 3 - Alpha

# <img src="https://www.gstatic.com/lamda/images/favicon_v1_150160cddff7f294ce30.svg" width="35px" alt="Gemini Icon" /> Gemini API



A Python wrapper, [python-gemini-api](https://pypi.org/project/python-gemini-api/), interacts with [Google Gemini](https://gemini.google.com) via reverse engineering.

<br>

## What is [Gemini](https://deepmind.google/technologies/gemini/#introduction)?
Gemini is a family of generative AI models developed by Google DeepMind that is designed for multimodal use cases. The Gemini API gives you access to the Gemini Pro and Gemini Pro Vision models. In February 2024, Google"s **Gemini** service was changed to **Gemini**. <br> [Paper](https://arxiv.org/abs/2312.11805), [Official Web](https://deepmind.google/technologies/gemini/#introduction), [Open-source Gemma-7b](https://huggingface.co/google/gemma-7b)

## Installation
```
pip install python-gemini-api
```
```
pip install git+https://github.com/dsdanielpark/Gemini-API.git
```

## Authentication

> **Warning** *DO NOT* expose your cookies. 

- Depending on the region and Google account status, *multiple cookies may be required*, including `__Secure-1PSIDTS`, `__Secure-1PSIDCC`, `__Secure-1PSID`, `NID`, *or more*.
- You must appropriately set the `cookies_dict` parameter to `Gemini` class.
- Cookie values can be changed frequently, thus it is recommended to automatically update them through the [browser_cookie3](https://github.com/borisbabic/browser_cookie3) package.

<br>

## Usage

### Innitiallization
```python
from gemini import Gemini

cookies = {
    "__Secure-1PSID": "value",
    "__Secure-1PSIDTS": "value",
    "__Secure-1PSIDCC": "value",
    "NID": "value",
}

GeminiClient = Gemini(cookies=cookies)
```
Or update cookies automatically using [broser_cookie3](https://github.com/borisbabic/browser_cookie3). However, this feature is incomplete, and you may need to periodically update cookie values in a .env file or json file. You will need to develop a logic that suits you for automatically updating cookies.
```python
from gemini import Gemini

GeminiClient = Gemini(auto_cookies=True)
```

<br>

### Text generation
```python
prompt = "Hello, Gemini. What's the weather like in Seoul today?"
response = GeminiClient.generate_content(prompt)
print(response)
```

### Image generation
```python
prompt = "Hello, Gemini. Give me a beautiful photo of Seoul's scenery."
response = GeminiClient.generate_content(prompt)

print("\n".join(response.images)) # Print images

for i, image in enumerate(response.images): # Save images
    image.save(path="folder_path/", filename=f"seoul_{i}.png")

```

### Generate contents about image
*It may not work as it is only available for certain accounts, regions, and other restrictions.*
As an experimental feature, it is possible to ask questions with an image. However, this functionality is only available for accounts with image upload capability in Gemini"s web UI. 

```python
prompt = "What is in the image?"
image = open("folder_path/image.jpg", "rb").read() # (jpeg, png, webp) are supported.

response = GeminiClient.generate_content(prompt, image)
```

### [Text To Speech(TTS)](https://cloud.google.com/text-to-speech?hl=ko) from Gemini
Business users and high traffic volume may be subject to account restrictions according to Google"s policies. Please use the [Official Google Cloud API](https://cloud.google.com/text-to-speech) for any other purpose. 
The user is solely responsible for all code, and it is imperative to consult Google"s official services and policies. Furthermore, the code in this repository is provided under the MIT license, and it disclaims any liability, including explicit or implied legal responsibilities.
```python
text = "Read this sentence: Hello, I'm developer in seoul"
response = GeminiClient.generate_content(prompt, image)
audio = GeminiClient.speech(text)
with open("speech.ogg", "wb") as f:
    f.write(bytes(audio["audio"]))with open("speech.ogg", "wb") as f:
```


## More Features
### Behind a proxy
If you are working behind a proxy, use the following.
```python
proxies = {
    "http": "http://proxy.example.com:8080",
    "https": "https://proxy.example.com:8080"
}

GeminiClient = Gemini(cookies=cookies, proxies=proxies, timeout=30)
GeminiClient.generate_content("Hello, Gemini. Give me a beautiful photo of Seoul"s scenery.")
```

### Use rotating proxies

If you want to **avoid blocked requests** and bans, then use [Smart Proxy by Crawlbase](https://crawlbase.com/docs/smart-proxy/?utm_source=github_ad&utm_medium=social&utm_campaign=bard_api). It forwards your connection requests to a **randomly rotating IP address** in a pool of proxies before reaching the target website. The combination of AI and ML make it more effective to **avoid CAPTCHAs and blocks**.

```python
# Get your proxy url at crawlbase https://crawlbase.com/docs/smart-proxy/get/
proxy_url = "http://xxxxx:@smartproxy.crawlbase.com:8012" 
proxies = {"http": proxy_url, "https": proxy_url}

GeminiClient = Gemini(cookies=cookies, proxies=proxies, timeout=30)
GeminiClient.generate_content("Hello, Gemini. Give me a beautiful photo of Seoul's scenery.")
```


### Reusable session object
You can continue the conversation using a reusable session. However, this feature is limited, and it is difficult for a package-level feature to perfectly maintain conversation_id and context. You can try to maintain the consistency of conversations same way as other LLM services, such as passing some sort of summary of past conversations to the DB.
```python
from gemini import Gemini, SESSION_HEADERS
import requests

cookies = {
    "__Secure-1PSID": "value",
    "__Secure-1PSIDTS": "value",
    "__Secure-1PSIDCC": "value",
    "NID": "value",
}

session = requests.Session()
session.headers = SESSION_HEADERS
session.cookies.update(cookies)

GeminiClient = Gemini(session=session, timeout=30)
response = GeminiClient.generate_content("Hello, Gemini. What's the weather like in Seoul today?")["content"]

# Continued conversation without set new session
response = GeminiClient.generate_content("What was my last prompt?")
```


<br>

## [More features](https://github.com/dsdanielpark/Gemini-API/blob/main/documents/README_DEV.md)
- [Chat Gemini](https://github.com/dsdanielpark/Gemini-API/blob/main/documents/README_DEV.md#chatbard)
- [Get image links](https://github.com/dsdanielpark/Gemini-API/blob/main/documents/README_DEV.md#get-image-links)
- [Multi-language Gemini](https://github.com/dsdanielpark/Gemini-API/blob/main/documents/README_DEV.md#multi-language-bard-api)
- [Export Conversation](https://github.com/dsdanielpark/Gemini-API/blob/main/documents/README_DEV.md#export-conversation)
- [Export Code to Repl.it](https://github.com/dsdanielpark/Gemini-API/blob/main/documents/README_DEV.md#export-code-to-replit)
- [Executing Python code received as a response from Gemini](https://github.com/dsdanielpark/Gemini-API/blob/main/documents/README_DEV.md#chatbard)
- [Max_token, Max_sentences](https://github.com/dsdanielpark/Gemini-API/blob/main/documents/README_DEV.md#max_token-max_sentence)
- [Translation to another programming language](https://github.com/dsdanielpark/Gemini-API/blob/main/documents/README_DEV.md#translation-to-another-programming-language)

<br>

## [FAQ](https://github.com/dsdanielpark/Gemini-API/blob/main/documents/README_FAQ.md)
You can find most help on the [FAQ](https://github.com/dsdanielpark/Gemini-API/blob/main/documents/README_FAQ.md) and [Issue](https://github.com/dsdanielpark/Gemini-API/issues) pages. Alternatively, utilize the official Gemini API at [Google AI Studio](https://ai.google.dev/tutorials/ai-studio_quickstart).

            
## [Issues](https://github.com/dsdanielpark/Gemini-API/issues)
Sincerely grateful for any reports on new features or bugs. Your valuable feedback on the code is highly appreciated. Frequent errors may occur due to changes in Google"s service API interface. Both [Issue reports](https://github.com/dsdanielpark/Gemini-API/issues) and [Pull requests](https://github.com/dsdanielpark/Gemini-API/pulls) contributing to improvements are always welcome. We strive to maintain an active and courteous open community.


## Contributors
We would like to express my sincere gratitude to all the contributors.

## Contacts
- **Core Maintainer:** Minwoo(Daniel) Park, [@dsdanielpark](https://github.com/dsdanielpark)
- **E-mail:** parkminwoo1991@gmail.com

## License
[MIT](https://opensource.org/license/mit/) license, 2024, Minwoo(Daniel) Park. We hereby strongly disclaim any explicit or implicit legal liability related to our works. Users are required to use this package responsibly and at their own risk.



## References
[1] Github [acheong08/Gemini](https://github.com/acheong08/Gemini) <br>
[2] Github [GoogleCloudPlatform/generative-ai](https://github.com/GoogleCloudPlatform/generative-ai) <br>
[3] Github [HanaokaYuzu/Gemini-API](https://github.com/HanaokaYuzu/Gemini-API) <br>
[4] [Google AI Studio](https://ai.google.dev/tutorials/ai-studio_quickstart) <br>



