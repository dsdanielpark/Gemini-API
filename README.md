Development Status :: 1 - Planning

*Not fully prepared yet.*

# <img src="https://www.gstatic.com/lamda/images/favicon_v1_150160cddff7f294ce30.svg" width="35px" alt="Gemini Icon" /> Google - Gemini API <a href="https://pypi.org/project/bardapi/"><img alt="PyPI" src="https://img.shields.io/pypi/v/python-gemini-api"></a>

A *unofficial* Python wrapper, [python-gemini-api](https://pypi.org/project/python-gemini-api/), operates through reverse-engineering, utilizing cookie values to interact with [Google Gemini](https://gemini.google.com) for users struggling with frequent authentication problems or unable to authenticate via [Google Authentication](https://developers.google.com/identity/protocols/oauth2?hl=en).

Collaborated competently with [Antonio Cheong](https://github.com/acheong08).


## What is [Gemini](https://deepmind.google/technologies/gemini/#introduction)?

[[Paper](https://arxiv.org/abs/2312.11805)] [[Official Website](https://deepmind.google/technologies/gemini/#introduction)] [[Official API](https://aistudio.google.com/)] [[API Documents](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini)]

Gemini is a family of generative AI models developed by Google DeepMind that is designed for multimodal use cases. The Gemini API gives you access to the Gemini Pro and Gemini Pro Vision models. In February 2024, Google's **Bard** service was changed to **Gemini**.

  - [Installation](#installation)
  - [Authentication](#authentication)
  - [Usage](#usage)
    - [Initialization](#initialization)
    - [Text generation](#text-generation)
    - [Image generation](#image-generation)
    - [Generate content with image](#generate-content-with-image)
    - [Text To Speech(TTS) from Gemini](#text-to-speechtts-from-gemini)
  - [Further](#further)
    - [Behind a proxy](#behind-a-proxy)
    - [Use rotating proxies](#use-rotating-proxies)
    - [Reusable session object](#reusable-session-object)
  - [More features](#more-features)



<br>



## Installation
```bash
pip install python-gemini-api
```
```bash
pip install git+https://github.com/dsdanielpark/Gemini-API.git
```

## Authentication
> [!NOTE]
> Cookies can change quickly. Don't reopen the same session or repeat prompts too often; they'll expire faster. If the cookie value doesn't export correctly, refresh the Gemini page and export again. Check this [sample cookie file](https://github.com/dsdanielpark/Gemini-API/blob/main/cookies.txt).
1. Visit https://gemini.google.com/ and wait for it to fully load.
2. *(Recommended)* Export gemini site cookies using a Chrome extension. Use [ExportThisCookies](https://chromewebstore.google.com/detail/exportthiscookie/dannllckdimllhkiplchkcaoheibealk), open and copy the txt file contents.

<details><summary>Further: For manual collection or Required for a few users upon error</summary>

3. For manual cookie collection, refer to [this image](assets/cookies.pdf). Press F12 → Network → Send any prompt to gemini webui → Click the post address starting with "https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate" → Headers → Request Headers → Cookie → Copy and Reformat as JSON manually.
4. *(Required for a few users upon error)* If errors persist after manually collecting cookies, refresh the Gemini website and collect cookies again. If errors continue, some users may need to manually set the nonce value. To do this: Press F12 → Network → Send any prompt to gemini webui → Click the post address starting with "https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate" → Payload → Form Data → Copy the "at" key value. See [this image](assets/nonce_value.pdf) for reference.
</details>

## Usage
After switching from Bard to Gemini, multiple region or Google account-based cookies, *frequently updated*, are necessary. 


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

# If you keep getting nonce errors, pass the nonce value. See the `Authentication.further` section above.
# GeminiClient = Gemini(cookies=cookies, nonce="value") 
```
Can update cookies automatically using [broser_cookie3](https://github.com/borisbabic/browser_cookie3). For the first attempt, manually download the cookies to test the functionality. (Currently in progress)

> [!IMPORTANT]
> *Before proceeding, ensure that the GeminiClient object is defined without any errors.*




### Text generation
```python
prompt = "Hello, Gemini. What's the weather like in Seoul today?"
response = GeminiClient.generate_content(prompt)
print(response)
```
> [!TIP]
> If the session fails to connect, works improperly, or terminates, returning an error, it is recommended to manually renew the cookies. The error is likely due to incorrect cookie values. Refresh or log out of Gemini web to renew cookies and try again. However, do not retry multiple times after one success to set session.

#### Parser

Gemini web returns responses from various 3rd party services, requiring different types of parsers. If all parsing methods fail, it returns the response's text as is.
Please refer to [gemini.models.parser.base](https://github.com/dsdanielpark/Gemini-API/blob/main/gemini/models/parser/base.py). The default parser attempted is [gemini.models.parser.methods](https://github.com/dsdanielpark/Gemini-API/blob/main/gemini/models/parser/methods.py), and you can also use custom parsers as arguments in `generate_content` like this.

<details><summary>How to use CustomParser</summary>
  
```python
class CustomParser(ResponseParser):
    def parse(self, response_text):
        """
        Implements custom parsing logic.

        Example logic: Simply returns the response_text as is.

        Args:
            response_text (str): The text to be parsed.

        Returns:
            str: The parsed (or in this case, unchanged) response text.
        """
        return parsed_response_text

prompt = "Hello, Gemini. What's the weather like in Seoul today?"
response = GeminiClient.generate_content(prompt, CustomParser)
```
</details>



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
- [Multi-language Gemini](https://github.com/dsdanielpark/Gemini-API/blob/main/documents/README_DEV.md#multi-language-bard-api)
- [Export Conversation](https://github.com/dsdanielpark/Gemini-API/blob/main/documents/README_DEV.md#export-conversation)
- [Export Code to Repl.it](https://github.com/dsdanielpark/Gemini-API/blob/main/documents/README_DEV.md#export-code-to-replit)
- [Executing Python code received as a response from Gemini](https://github.com/dsdanielpark/Gemini-API/blob/main/documents/README_DEV.md#chatbard)
- [Max_token, Max_sentences](https://github.com/dsdanielpark/Gemini-API/blob/main/documents/README_DEV.md#max_token-max_sentence)

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

> *Warning**
Users bear all legal responsibilities when using the GeminiAPI package, which offers easy access to Google Gemini for developers. This unofficial Python package isn't affiliated with Google and may lead to Google account restrictions if used excessively or commercially due to its reliance on Google account cookies. Frequent changes in Google's interface, Google's API policies, and your country/region, as well as the status of your Google account, may affect functionality. Utilize the issue page and discussion page.

<br>


*Copyright (c) 2024 Minwoo(Daniel) Park, South Korea*<br>
