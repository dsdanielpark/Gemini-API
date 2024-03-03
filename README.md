Development Status :: 2 - Pre-Alpha

*Not fully prepared yet.*

# <img src="https://www.gstatic.com/lamda/images/favicon_v1_150160cddff7f294ce30.svg" width="35px" alt="Gemini Icon" /> Google - Gemini API
A Python wrapper, [python-gemini-api](https://pypi.org/project/python-gemini-api/), interacts with [Google Gemini](https://gemini.google.com) via reverse engineering. Reconstructing with REST syntax for users facing frequent authentication errors or unable to authenticate properly in [Google Authentication](https://developers.google.com/identity/protocols/oauth2?hl=ko).

Collaborated competently with [Antonio Cheong](https://github.com/acheong08).


## What is [Gemini](https://deepmind.google/technologies/gemini/#introduction)?
Gemini is a family of generative AI models developed by Google DeepMind that is designed for multimodal use cases. The Gemini API gives you access to the Gemini Pro and Gemini Pro Vision models. In February 2024, Google's **Bard** service was changed to **Gemini**. [Paper](https://arxiv.org/abs/2312.11805), [Official Website](https://deepmind.google/technologies/gemini/#introduction), [Official API](https://aistudio.google.com/), [API Documents](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini).

- [Google - Gemini API](#-google---gemini-api)
  - [What is Gemini?](#what-is-gemini)
  - [Installation](#installation)
  - [Authentication](#authentication)
  - [Usage](#usage)
  - [Further](#further)
  - [More features](#more-features)
  - [How to use open-source Gemma](#how-to-use-open-source-gemma)
  - [FAQ](#faq)


<br>



## Installation
```
pip install python-gemini-api
```
```
pip install git+https://github.com/dsdanielpark/Gemini-API.git
```

## Authentication
> [!NOTE]
> Cookies can change quickly. Don't reopen the same session or repeat prompts too often; they'll expire faster. If the cookie value doesn't export correctly, refresh the Gemini page and export again. Check this [sample cookie file](https://github.com/dsdanielpark/Gemini-API/blob/main/cookies.txt).
1. Go to https://gemini.google.com/ and wait for it to load.
2. *(Recommended)* While on the gemini website, export cookies using a Chrome extension. If using [ExportThisCookies](https://chromewebstore.google.com/detail/exportthiscookie/dannllckdimllhkiplchkcaoheibealk) extension, open the downloaded txt file and copy its contents exactly as they are. 
3. Or, press F12 → Network → Send prompt to webui gemini → Click post address starting with "https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate" → Copy cookies → Format as a dictionary manually. Refer to this [image](assets/netrwork.pdf).

## Usage
After changed Bard to Gemini, multiple cookies, *often updated*, are needed based on region or Google account. Thus, automatic cookie renewal logic is crucial.
### Initialization
You must appropriately set the `cookies_dict` parameter to `Gemini` class. When using the `auto_cookies` argument to automatically collect cookies, keep the [Gemini web page](https://gemini.google.com/) opened that receives Gemini's response open in your web browser.<br>

```python
from gemini import Gemini

cookies = {
    "key": "value"
}

GeminiClient = Gemini(cookies=cookies)
# GeminiClient = Gemini(cookie_fp="folder/cookie_file.json") # Or use cookie file path
# GeminiClient = Gemini(auto_cookies=True) # Or use auto_cookies paprameter
```
Can update cookies automatically using [broser_cookie3](https://github.com/borisbabic/browser_cookie3). For the first attempt, manually download the cookies to test the functionality.

> [!IMPORTANT]
> *Before proceeding, ensure that the GeminiClient object is defined without any errors.*
<br>

### Text generation
```python
prompt = "Hello, Gemini. What's the weather like in Seoul today?"
response = GeminiClient.generate_content(prompt)
print(response)
```

### Image generation

```
prompt = "Hello, Gemini. Give me a beautiful photo of Seoul's scenery."
response = GeminiClient.generate_content(prompt)

print("\n".join(response.images)) # Print images

for i, image in enumerate(response.images): # Save images
    image.save(path="folder_path/", filename=f"seoul_{i}.png")

```

### Generate content with image

As an experimental feature, it is possible to ask questions with an image. However, this functionality is only available for accounts with image upload capability in Gemini's web UI. 

```
prompt = "What is in the image?"
image = open("folder_path/image.jpg", "rb").read() # (jpeg, png, webp) are supported.

response = GeminiClient.generate_content(prompt, image)
```

### [Text To Speech(TTS)](https://cloud.google.com/text-to-speech?hl=ko) from Gemini
Business users and high traffic volume may be subject to account restrictions according to Google's policies. Please use the [Official Google Cloud API](https://cloud.google.com/text-to-speech) for any other purpose. 
```
text = "Hello, I'm developer in seoul" # Gemini will speak this sentence
response = GeminiClient.generate_content(prompt)
audio = GeminiClient.speech(text)
with open("speech.ogg", "wb") as f:
    f.write(bytes(audio["audio"]))
```

<br>

## Further
### Behind a proxy
If you are working behind a proxy, use the following.
```python
proxies = {
    "http": "http://proxy.example.com:8080",
    "https": "https://proxy.example.com:8080"
}

GeminiClient = Gemini(cookies=cookies, proxies=proxies, timeout=30)
GeminiClient.generate_content("Hello, Gemini. Give me a beautiful photo of Seoul's scenery.")
```

### Use rotating proxies

If you want to **avoid blocked requests** and bans, then use [Smart Proxy by Crawlbase](https://crawlbase.com/docs/smart-proxy/?utm_source=github_ad&utm_medium=social&utm_campaign=bard_api). It forwards your connection requests to a **randomly rotating IP address** in a pool of proxies before reaching the target website. The combination of AI and ML make it more effective to avoid CAPTCHAs and blocks.

```python
# Get your proxy url at crawlbase https://crawlbase.com/docs/smart-proxy/get/
proxy_url = "http://xxxxx:@smartproxy.crawlbase.com:8012" 
proxies = {"http": proxy_url, "https": proxy_url}

GeminiClient = Gemini(cookies=cookies, proxies=proxies, timeout=30)
GeminiClient.generate_content("Hello, Gemini. Give me a beautiful photo of Seoul's scenery.")
```


### Reusable session object
You can continue the conversation using a reusable session. However, this feature is limited, and it is difficult for a package-level feature to perfectly maintain context. You can try to maintain the consistency of conversations same way as other LLM services, such as passing some sort of summary of past conversations to the DB.
```python
from gemini import Gemini, HEADERS
import requests

cookies = {
    "key": "value"
}

session = requests.Session()
session.headers = HEADERS
session.cookies.update(cookies)

GeminiClient = Gemini(session=session, timeout=30)
response = GeminiClient.generate_content("Hello, Gemini. What's the weather like in Seoul today?")

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


## How to use open-source [Gemma](https://huggingface.co/google/gemma-7b)
[Gemma](https://huggingface.co/google/gemma-7b) models are Google's lightweight, advanced text-to-text, decoder-only language models, derived from Gemini research. Available in English, they offer open weights and variants, ideal for tasks like question answering and summarization. Their small size enables deployment in resource-limited settings, broadening access to cutting-edge AI. For more infomation, visit [Gemma-7b](https://huggingface.co/google/gemma-7b) model card.

```python
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("google/gemma-7b")
model = AutoModelForCausalLM.from_pretrained("google/gemma-7b")

input_text = "Write me a poem about Machine Learning."
input_ids = tokenizer(input_text, return_tensors="pt")

outputs = model.generate(**input_ids)
print(tokenizer.decode(outputs[0]))
```





## Sponsor
Use [Crawlbase](https://crawlbase.com/) API for efficient data scraping to train AI models, boasting a 98% success rate and 99.9% uptime. It's quick to start, GDPR/CCPA compliant, supports massive data extraction, and is trusted by 70k+ developers.

[<img src="assets/crawlbase_logo.png" width="300">](https://crawlbase.com/)



## [FAQ](https://github.com/dsdanielpark/Gemini-API/blob/main/documents/README_FAQ.md)
You can find most help on the [FAQ](https://github.com/dsdanielpark/Gemini-API/blob/main/documents/README_FAQ.md) and [Issue](https://github.com/dsdanielpark/Gemini-API/issues) pages. Alternatively, utilize the official Gemini API at [Google AI Studio](https://ai.google.dev/tutorials/ai-studio_quickstart).

            
## [Issues](https://github.com/dsdanielpark/Gemini-API/issues)
Sincerely grateful for any reports on new features or bugs. Your valuable feedback on the code is highly appreciated. Frequent errors may occur due to changes in Google's service API interface. Both [Issue reports](https://github.com/dsdanielpark/Gemini-API/issues) and [Pull requests](https://github.com/dsdanielpark/Gemini-API/pulls) contributing to improvements are always welcome. We strive to maintain an active and courteous open community.


## Contributions
We would like to express our sincere gratitude to all the contributors.


<details><summary>Further development potential</summary>
  
- [ ] `refactoring`
- [x] `gemini/core`: httpx.session
  - [x] `messages`
      - [x] `content`
        - [x] `text`  
          - [ ] `parsing`
        - [ ] `image`
          - [ ] `parsing`
      - [ ] `response format structure class`
      - [ ] `tool_calls`
  - [ ] `third party`
    - [ ] `replit`
    - [ ] `google tools`
- [ ] `gemini/client`: httpx.AsyncClient
  - [ ] `messages`
      - [ ] `content`
        - [ ] `text`  
          - [ ] `parsing`
        - [ ] `image`
          - [ ] `parsing`
      - [ ] `response format structure class`
      - [ ] `tool_calls`
  - [ ] `third party`
    - [ ] `replit`
    - [ ] `google tools`   
</details>

## Contacts
Core maintainers:
- [Antonio Cheong](https://github.com/acheong08) / teapotv8@proton.me <br>
- [Daniel Park](https://github.com/DSDanielPark) / parkminwoo1991@gmail.com
 


## License
[MIT](https://opensource.org/license/mit/) license, 2024, Minwoo(Daniel) Park. We hereby strongly disclaim any explicit or implicit legal liability related to our works. Users are required to use this package responsibly and at their own risk. This project is a personal initiative and is not affiliated with or endorsed by Google. It is recommended to use Google's official API.



## References
[1] Github [acheong08/Bard](https://github.com/acheong08/Bard) <br>
[2] Github [dsdanielpark/Bard-API](https://github.com/dsdanielpark/Bard-API) <br>
[3] Github [GoogleCloudPlatform/generative-ai](https://github.com/GoogleCloudPlatform/generative-ai) <br>
[4] [Google AI Studio](https://ai.google.dev/tutorials/ai-studio_quickstart) <br>

> [!WARNING]
> Users bear all legal responsibilities when using the GeminiAPI package, which offers easy access to Google Gemini for developers. This unofficial Python package isn't affiliated with Google and may lead to Google account restrictions if used excessively or commercially due to its reliance on Google account cookies. Frequent changes in Google's interface, Google's API policies, and your country/region, as well as the status of your Google account, may affect functionality. Utilize the issue page and discussion page.

<br>


*Copyright (c) 2024 Minwoo(Daniel) Park, South Korea*<br>
