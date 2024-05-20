Development Status :: 3 - Alpha


# GitHub installation required for the following features.
```
pip install git+https://github.com/dsdanielpark/Gemini-API.git
```

This section aims to implement functionalities of the Gemini API. While there are many readily portable codes, updates may be delayed.


# Contents
- [GitHub installation required for the following features.](#github-installation-required-for-the-following-features)
- [Contents](#contents)
    - [Chat Gemini](#chat-gemini)
    - [Multi-language Gemini](#multi-language-gemini)
    - [Get image links](#get-image-links)
    - [Export Conversation](#export-conversation)
    - [Export Code to Repl.it](#export-code-to-replit)
    - [Executing Python code received as a response from Gemini](#executing-python-code-received-as-a-response-from-gemini)
    - [Using Gemini asynchronously](#using-gemini-asynchronously)
    - [Translation to Another Programming Language](#translation-to-another-programming-language)
    - [Post-processing: max\_token, max\_sentence](#post-processing-max_token-max_sentence)
  - [Release Notes](#release-notes)
      - [v2.4.7](#v247)
      - [v2.4.8](#v248)


### Chat Gemini

```python

```


### Multi-language Gemini
For commercial use cases, please refrain from using the unofficial Google Translate package included in `python-gemini-api` for non-commercial purposes. Instead, kindly visit the official Google Cloud Translation website. Please use it responsibly, taking full responsibility for your actions, as `python-gemini-api` package does not assume any implicit or explicit liability.
> Official Google Translation API
- Support Languages: https://cloud.google.com/translate/docs/languages?hl=ko
> Unofficial Google Trnaslator for non-profit purposes (such as feature testing)
- Support Languages: https://github.com/nidhaloff/deep-translator/blob/master/deep_translator/constants.py
```python

```

<br>

### Get image links
```python

```

<br>
    
<br>    

### Export Conversation
*It may not work as it is only available for certain accounts, regions, and other restrictions.*
Gemini UI offers a convenient way to share a specific answer from Gemini by generating a URL. This feature enables users to easily create and share URLs for individual answers.

```python


```

<br>

### Export Code to [Repl.it](https://replit.com/)
```python

```

<br>

### Executing Python code received as a response from Gemini
```python
```
    
<br>

### Using Gemini asynchronously 
Using asynchronous implementation will be efficient when implementing ChatBots or something alone those lines.    
GeminiAsync is not using requests library instead it is using httpx library and http2 protocol.
    
```python

```

<br>
    



### Translation to Another Programming Language
Please check the translation results in [this folder](https://github.com/dsdanielpark/Gemini-API/tree/main/translate_to).
- Copy the code of [Core.py](https://github.com/dsdanielpark/Gemini-API/blob/17d5e948d4afc535317de3964232ab82fe223521/`python-gemini-api`/core.py).
- Ask ChatGPT to translate like "Translate to Swift."
- Ask ChatGPT to optimize the code or provide any desired instructions until you're satisfied.<br>

![](./assets/translate.png)


<br>

### Post-processing: max_token, max_sentence
Gemini does not support temperature or hyperparameter adjustments, but it is possible to achieve the appearance of limiting the number of output tokens or the number of output sentences using simple algorithms, as follows:
```python
from gemini import Gemini

cookies = {
    "key": "value"
}

GeminiClient = Gemini(cookies=cookies)
# GeminiClient = Gemini(cookie_fp="folder/cookie_file.json") # Or use cookie file path
# GeminiClient = Gemini(auto_cookies=True) # Or use auto_cookies paprameter

prompt = "Hello, Gemini. What's the weather like in Seoul today?"
response = GeminiClient.generate_content(prompt)

# max_token==30
max_token(response, 30) 
# max_sentence==2
max_sentence(response, 2)
```

<br>



## Release Notes
Write a rough draft of the Gemini API release notes.

#### v2.4.7 
- Fixed missing aiohttp dependency for open router async client
- Cleaned up requirements import.

#### v2.4.8
- Add verification(`verify`) argument in `Gemini` class.
- Add cookies argument in `GeminiImage` class.

#### v2.4.9 ~ v2.4.11
- Writes mostly private test code for errors and tests functionality.
- Rechecks robust implementation of parsing methods.
- Preparing to upgrade to major version three after a small patch.
