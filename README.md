
<div align="right">
  </div>

# <img src="https://www.gstatic.com/lamda/images/favicon_v1_150160cddff7f294ce30.svg" width="35px" alt="Gemini Icon" /> Gemini API  <a href="https://pypi.org/project/python-gemini-api/"> <img alt="PyPI" src="https://img.shields.io/pypi/v/python-gemini-api?color=black"></a>



https://github.com/dsdanielpark/Gemini-API/assets/81407603/e0c11d4f-3fe1-4cbb-ba79-d9f89b637324



A *unofficial* Python wrapper, [python-gemini-api](https://pypi.org/project/python-gemini-api/), operates through reverse-engineering, utilizing cookie values to interact with [Google Gemini](https://gemini.google.com) for users struggling with frequent authentication problems or unable to authenticate via [Google Authentication](https://developers.google.com/identity/protocols/oauth2?hl=en).

Collaborated competently with [Antonio Cheong](https://github.com/acheong08).





<br>


- [ Gemini API   ](#-gemini-api---)
  - [What is Gemini?](#what-is-gemini)
  - [Installation](#installation)
  - [Authentication](#authentication)
  - [Usage](#usage)
    - [# 01. Initialization](#-01-initialization)
    - [# 02. Generate content](#-02-generate-content)
    - [# 03. Text generation](#-03-text-generation)
    - [# 04. Image generation](#-04-image-generation)
    - [# 05. Retrieving Images from Gemini Responses](#-05-retrieving-images-from-gemini-responses)
    - [# 06. Generate content from images](#-06-generate-content-from-images)
    - [# 07. Generate content using Google Services](#-07-generate-content-using-google-services)
    - [# 08. Fix context setting rcid](#-08-fix-context-setting-rcid)
    - [# 09. Changing the Selected Response from 0 to n](#-09-changing-the-selected-response-from-0-to-n)
    - [# 10. Generate custom content](#-10-generate-custom-content)
  - [More features](#more-features)
  - [Open-source LLM, Gemma](#open-source-llm-gemma)
    - [How to use Gemma](#how-to-use-gemma)






<br>


## What is [Gemini](https://deepmind.google/technologies/gemini/#introduction)?

| [Paper](https://arxiv.org/abs/2312.11805) | [Official Website](https://deepmind.google/technologies/gemini/#introduction) | [Official API](https://aistudio.google.com/) | [API Documents](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini) |

Gemini is a family of generative AI models developed by Google DeepMind that is designed for multimodal use cases. The Gemini API gives you access to the Gemini Pro and Gemini Pro Vision models. In February 2024, Google's **Bard** service was changed to **Gemini**.



## Installation
```
pip install python-gemini-api
```
```
pip install git+https://github.com/dsdanielpark/Gemini-API.git
```
For the updated version, use as follows:
```
pip install -q -U python-gemini-api
```
## Authentication
> [!NOTE]
> Cookies can change quickly. Don't reopen the same session or repeat prompts too often; they'll expire faster. If the cookie value doesn't export correctly, refresh the Gemini page and export again. 
1. Visit https://gemini.google.com/ <br>
    With browser open, try auto-collecting cookies first.
    ```python
    from gemini import Gemini
    GeminiClient = Gemini(auto_cookies=True)
    # GeminiClient = Gemini(auto_cookies=True, target_cookies = ["__Secure-1PSID", "__Secure-1PSIDTS"]) # Can select cookies.
    response = GeminiClient.generate_content("Hello, Gemini. What's the weather like in Seoul today?")
    print(response.payload)
    ```
2. *(Manually)* `F12` for browser console → `Session: Application` → `Cookies` → Copy the value of some working cookie sets. If it doesn't work, go to step 3.
    <details><summary>Some working cookie sets</summary>
    Cookies may vary by account or region. 
      
    First try `__Secure-1PSIDCC` alone. If it doesn't work, use `__Secure-1PSID` and `__Secure-1PSIDTS`. Still no success? Try these four cookies: `__Secure-1PSIDCC`, `__Secure-1PSID`, `__Secure-1PSIDTS`, `NID`. If none work, proceed to step 3 and consider sending the entire cookie file.
    
    </details>

3. *(Recommended)* Export Gemini site cookies via a browser extension. For instance, use Chrome extension [ExportThisCookies](https://chromewebstore.google.com/detail/exportthiscookie/dannllckdimllhkiplchkcaoheibealk), open, and copy the txt file contents.

<details><summary>Further: For manual collection or Required for a few users upon error</summary>

4. For manual cookie collection, refer to [this image](assets/cookies.pdf). Press F12 → Network → Send any prompt to Gemini webui → Click the post address starting with "https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate" → Headers → Request Headers → Cookie → Copy and Reformat as JSON manually.
5. *(Required for a few users upon error)* If errors persist after manually collecting cookies, refresh the Gemini website and collect cookies again. If errors continue, some users may need to manually set the nonce value. To do this: Press F12 → Network → Send any prompt to Gemini webui → Click the post address starting with "https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate" → Payload → Form Data → Copy the "at" key value. See [this image](assets/nonce_value.pdf) for reference.
</details>


> [!IMPORTANT] 
>  Try different Google accounts until you find a working cookie. Use a fresh browser to ensure no remaining cookie values. Use secret browsing mode with independent cookies. Results may vary depending on factors like IP and account status. Providing the entire set of cookies seems to fix one cookie per account. Additionally, once successfully connected with that cookie, it seems to work flawlessly for over three weeks without any errors. *Try various methods until you succeed. Experiment in different environments.*


<br>

## Usage

*Simple usage*

Setting Gemini Response Language (Optional): Check supported languages [here](https://developers.google.com/hotels/hotel-prices/dev-guide/country-codes). Default is English.

```python
import os
os.environ["GEMINI_LANGUAGE"] = "KR"
```

Generate content
```python
from gemini import Gemini

cookies = {} # Cookies may vary by account or region. Consider sending the entire cookie file.
GeminiClient = Gemini(cookies=cookies) # You can use various args

response = GeminiClient.generate_content("Hello, Gemini. What's the weather like in Seoul today?")
response.response_dict # renamed to payload after v2.3.0
```

Generate content from image
```python
from gemini import Gemini

cookies = {} # Cookies may vary by account or region. Consider sending the entire cookie file.

GeminiClient = Gemini(cookies=cookies) # You can use various args
response = GeminiClient.generate_content("What does the text in this image say?", image='folder/image.jpg')
response.response_dict # renamed to payload after v2.3.0
```

> [!NOTE] 
> If the generate_content method returns an empty payload, try executing it again without reinitializing the Gemini object.


<br>

### # 01. Initialization
Please explicitly declare `cookies` in dict format. You can also enter the path to the file containing the cookie with `cookie_fp`(*.json, *.txt supported). Check this [sample cookie file](https://github.com/dsdanielpark/Gemini-API/blob/main/cookies.txt).




```python
from gemini import Gemini

cookies = {
    "__Secure-1PSIDCC" : "value",
    "__Secure-1PSID" : "value",
    "__Secure-1PSIDTS" : "value",
    "NID" : "value",
    # Cookies may vary by account or region. Consider sending the entire cookie file.
  }

GeminiClient = Gemini(cookies=cookies)
# GeminiClient = Gemini(cookie_fp="folder/cookie_file.json") # Or use cookie file path
# GeminiClient = Gemini(auto_cookies=True) # Or use auto_cookies paprameter
```

#### Auto Cookie Update
For `auto_cookie` to be set to `True`, Gemini WebUI must be active in the browser. The [browser_cookie3](https://github.com/borisbabic/browser_cookie3) enables automatic cookie collection, though updates may not be complete yet.


> [!IMPORTANT]
>  **If the session connects successfully and `generate_content` runs well, CLOSE Gemini website.** If Gemini web stays open in the browser, cookies may expire faster.

<br>

### # 02. Generate content
Returns Gemini's response, but the first one might be empty. If generate_content yields an empty payload, rerun it without reinitializing Gemini. 

Regardless of model output type, access the response_dict property (renamed to payload after v2.3.0).
https://github.com/dsdanielpark/Gemini-API/blob/fdf064c57bc1fb47fbbb4b93067618a200e77f62/gemini/core.py#L252
```python
prompt = "Hello, Gemini. What's the weather like in Seoul today?"
response = GeminiClient.generate_content(prompt)
print(response.response_dict) # renamed to payload after v2.3.0
```
> [!IMPORTANT]
>  Once connected and generating valid content, **Be sure to CLOSE the Gemini website or CLOSE your browser** for cookie stability. 

<br>

The output of the generate_content function is `GeminiModelOutput`, with the following structure:

**Properties of GeminiModelOutput:**
- *rcid*: returns the response candidate id of the chosen candidate.
- *text*: returns the text of the chosen candidate.
- *code*: returns the codes of the chosen candidate.
- *web_images*: returns a list of web images from the chosen candidate.
- *generated_images*: returns a list of generated images from the chosen candidate.
- *payload*: returns the response dictionary, if available. (same as *reponse_dict* under v2.3.0)

https://github.com/dsdanielpark/Gemini-API/blob/fdf064c57bc1fb47fbbb4b93067618a200e77f62/gemini/src/model/output.py#L16


> [!NOTE]
> If the session fails to connect, works improperly, or terminates, returning an error, it is recommended to manually renew the cookies. The error is likely due to incorrect cookie values. Refresh or log out of Gemini web to renew cookies and try again. 

<br>

### # 03. Text generation
Returns text generated by Gemini.
```python
prompt = "Hello, Gemini. What's the weather like in Seoul today?"
response = GeminiClient.generate_content(prompt)
print(response.text)
```


<br>

### # 04. Image generation
Returns images generated by Gemini.
https://github.com/dsdanielpark/Gemini-API/blob/fdf064c57bc1fb47fbbb4b93067618a200e77f62/gemini/src/model/image.py#L12

*Sync downloader*
```python
from gemini import Gemini, GeminiImage

response = GeminiClient.generate_content("Create illustrations of Seoul, South Korea.")
generated_images = response.generated_images # Check generated images [Dict]

GeminiImage.save_sync(generated_images, save_path="save_dir", cookies=cookies)

# You can use byte type image dict for printing images as follow:
# bytes_images_dict = GeminiImage.fetch_images_dict_sync(generated_images, cookies=cookies) # Get bytes images dict
# GeminiImage.save_images_sync(bytes_images_dict, path="save_dir", cookies=cookies) # Save to path
```

<details><summary>Display images in IPython</summary>
  
  You can display the image or transmit it to another application in byte format.
  
  ```
  bytes_images_dict = GeminiImage.fetch_images_dict_sync(generated_images, cookies) # Get bytes images dict
  from IPython.display import display, Image
  import io
  
  for image_name, image_bytes in bytes_images_dict.items():
      print(image_name)
      image = Image(data=image_bytes)
      display(image)
  ```

</details>



*Async downloader*

```python
response = GeminiClient.generate_content("Create illustrations of Seoul, South Korea.")

generated_images = response.generated_images # Check generated images [Dict]

await GeminiImage.save(generated_images, "save_dir", cookies=cookies)
# image_data_dict = await GeminiImage.fetch_images_dict(generated_images, cookies=cookies)
# await GeminiImage.save_images(image_data_dict, "save_dir")
```


<details><summary>Async downloader wrapper</summary>

```
import asyncio
from gemini import Gemini, GeminiImage

async def save_generated_imagse(generated_imagse, save_path="save_dir", cookies=cookies):
    await GeminiImage.save(generated_imagse, save_path=save_path, cookies=cookies)

# Run the async function
if __name__ == "__main__":
    cookies = {"key" : "value"}
    generated_imagse = response.generated_imagse  
    asyncio.run(save_generated_imagse(generated_imagse, save_path="save_dir", cookies=cookies))
```

`GeminiImage.save` method logic

```
import asyncio
from gemini import Gemini, GeminiImage

async def save_generated_imagse(generated_imagse, save_path="save_dir", cookies=cookies):
    image_data_dict = await GeminiImage.fetch_images_dict(generated_imagse, cookies=cookies)  # Get bytes images dict asynchronously
    await GeminiImage.save_images(image_data_dict, save_path=save_path)  

# Run the async function
if __name__ == "__main__":
    cookies = {"key" : "value"}
    generated_imagse = response.generated_imagse  # Check response images [Dict]
    asyncio.run(save_generated_imagse(generated_imagse, save_path="save_dir", cookies=cookies))
```

</details>

> [!NOTE]
> Use GeminiImage for image processing. `web_images` works without cookies, but for images like `generated_image` from Gemini, pass cookies. Cookies are needed to download images from Google's storage. Check the response or use existing cookies variable.

<br>

### # 05. Retrieving Images from Gemini Responses
Returns images in response of Gemini.

*Sync downloader*
```python
from gemini import Gemini, GeminiImage

response = GeminiClient.generate_content("Please recommend a travel itinerary for Seoul.")
response_images = response.web_images # Check response images [Dict]

GeminiImage.save_sync(response_images, save_path="save_dir")

# You can use byte type image dict as follow:
# bytes_images_dict = GeminiImage.fetch_bytes_sync(response_images, cookies) # Get bytes images dict
# GeminiImage.save_images_sync(bytes_images_dict, path="save_dir") # Save to path
```
*Async downloader*
```python
response = GeminiClient.generate_content("Create illustrations of Seoul, South Korea.")

response_images = response.web_images # Check generated images [Dict]

await GeminiImage.save(response_images, "save_dir")
# image_data_dict = await GeminiImage.fetch_images_dict(response_images)
# await GeminiImage.save_images(image_data_dict, "save_dir")
```

<details><summary>Async downloader wrapper</summary>

```
import asyncio
from gemini import Gemini, GeminiImage

async def save_response_web_imagse(response_images, save_path="save_dir", cookies=cookies):
    await GeminiImage.save(response_images, save_path=save_path, cookies=cookies)

# Run the async function
if __name__ == "__main__":
    cookies = {"key" : "value"}
    response_images = response.web_images  
    asyncio.run(save_response_web_imagse(response_images, save_path="save_dir", cookies=cookies))
```

`GeminiImage.save` method logic

```
import asyncio
from gemini import Gemini, GeminiImage

async def save_response_web_imagse(response_images, save_path="save_dir", cookies=cookies):
    image_data_dict = await GeminiImage.fetch_images_dict(response_images, cookies=cookies)  # Get bytes images dict asynchronously
    await GeminiImage.save_images(image_data_dict, save_path=save_path)  

# Run the async function
if __name__ == "__main__":
    response_images = response.web_images  # Check response images [Dict]
    asyncio.run(save_response_web_imagse(response_images, save_path="save_dir", cookies=cookies))
```

</details>

<br>

### # 06. Generate content from images
Takes an image as input and returns a response.

```python
image = 'folder/image.jpg'
# image = open('folder/image.jpg', 'rb').read() # (jpg, jpeg, png, webp) are supported.

response = GeminiClient.generate_content("What does the text in this image say?", image=image)
response.response_dict
```

<br>

### # 07. Generate content using Google Services
To begin, you must link Google Workspace to activate this extension via the [Gemini web extension](https://gemini.google.com/extensions). Please refer to the [official notice](https://support.google.com/gemini/answer/13695044) and review the [privacy policies](https://support.google.com/gemini/answer/13594961?visit_id=638457301410420313-1578971242&p=privacy_help&rd=1) for more details.

*extention flags*
```
@Gmail, @Google Drive, @Google Docs, @Google Maps, @Google Flights, @Google Hotels, @YouTube
```
```python
response = GeminiClient.generate_content("@YouTube Search clips related with Google Gemini")
response.response_dict
```
<details><summary>Extension description</summary>
  
- Google Workspace
  - Services: **@Gmail, @Google Drive, @Google Docs** 
  - Description: Summarize, search, and find desired information quickly in your content for efficient personal task management.
  - Features: Information retrieval, document summarization, information categorization

- Google Maps
  - Service: **@Google Maps**
  - Description: Execute plans using location-based information. Note: Google Maps features may be limited in some regions.
  - Features: Route guidance, nearby search, navigation

- Google Flights
  - Service: **@Google Flights**
  - Description: Search real-time flight information to plan tailored travel itineraries.
  - Features: Holiday preparation, price comparison, trip planning

- Google Hotels
  - Service: **@Google Hotels**
  - Description: Search for hotels considering what matters most to you, like having a conversation with a friend.
  - Features: Packing for travel, sightseeing, special relaxation

- YouTube
  - Service: **@YouTube**
  - Description: Explore YouTube videos and ask questions about what interests you.
  - Features: Problem-solving, generating ideas, search, exploring topics
</details>

<br>


### # 08. Fix context setting rcid
You can specify a particular response by setting its response candidate id(rcid).

```python
# Generate content for the prompt "Give me some information about the USA."
response1 = GeminiClient.generate_content("Give me some information about the USA.")
# After reviewing the responses, choose the one you prefer and copy its RCID.
GeminiClient.rcid = "rc_xxxx"

# Now, generate content for the next prompt "How long does it take from LA to New York?"
response2 = GeminiClient.generate_content("How long does it take from LA to New York?")
```

<br>

### # 09. Changing the Selected Response from 0 to *n*
In Gemini, generate_content returns the first response. This may vary depending on length or sorting. Therefore, you can specify the index of the chosen response from 0 to *n* as follows. However, if there is only one response, revert it back to 0.
```python
from gemini import GeminiModelOutput
GeminiModelOutput.chosen = 1 # default is 0
response1 = GeminiClient.generate_content("Give me some information about the USA.")
```

<br>

### # 10. Generate custom content 
Parse the response text to extract desired values.

https://github.com/dsdanielpark/Gemini-API/blob/fdf064c57bc1fb47fbbb4b93067618a200e77f62/gemini/core.py#L317

Using `Gemini.generate_custom_content`, specify custom parsing to extract specific values. Utilize ParseMethod1 and ParseMethod2 by default, and you can pass custom parsing methods as arguments if desired. Refer to [custom_parser.py](https://github.com/dsdanielpark/Gemini-API/blob/main/gemini/src/parser/custom_parser.py).

```python
# You can create a parser method that takes response_text as the input for custom_parser.
response_text, response_status = GeminiClient.send_request("Give me some information about the USA.")

# Use custom_parser function or class inheriting from BaseParser
response = GeminiClient.generate_custom_content("Give me some information about the USA.", *custom_parser)
```

<br>

## Further

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
For standard cases, use Gemini class; for exceptions, use session objects. When creating a new bot Gemini server, adjust Headers.MAIN.
```python
from gemini import Gemini, Headers
import requests

cookies = {} 

session = requests.Session()
session.headers = Headers.MAIN
for key, value in cookies.items():
    session.cookies.update({key: value})

GeminiClient = Gemini(session=session) # You can use various args
response = GeminiClient.generate_content("Hello, Gemini. What's the weather like in Seoul today?")
```




<br>

## [More features](https://github.com/dsdanielpark/Gemini-API/blob/main/documents/README_DEV.md)
Explore additional features in [this document](https://github.com/dsdanielpark/Gemini-API/blob/main/documents/README_DEV.md).

If you want to develop your own simple code, you can start from [this simple code example](https://github.com/dsdanielpark/Gemini-API/blob/main/script/sample.ipynb).  

<br>


## Open-source LLM, [Gemma](https://huggingface.co/google/gemma-7b)
If you have sufficient GPU resources, you can download weights directly instead of using the Gemini API to generate content. Consider Gemma, an open-source model **available for on-premises use**.

[Gemma](https://huggingface.co/google/gemma-7b) models are Google's lightweight, advanced text-to-text, decoder-only language models, derived from Gemini research. Available in English, they offer open weights and variants, ideal for tasks like question answering and summarization. Their small size enables deployment in resource-limited settings, broadening access to cutting-edge AI. For more infomation, visit [Gemma-7b](https://huggingface.co/google/gemma-7b) model card.

### How to use Gemma
```python
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("google/gemma-7b")
model = AutoModelForCausalLM.from_pretrained("google/gemma-7b")

input_text = "Write me a poem about Machine Learning."
input_ids = tokenizer(input_text, return_tensors="pt")

outputs = model.generate(**input_ids)
print(tokenizer.decode(outputs[0]))
```

<br>


## [FAQ](https://github.com/dsdanielpark/Gemini-API/blob/main/documents/README_FAQ.md)
First review [HanaokaYuzu/Gemini-API](https://github.com/HanaokaYuzu/Gemini-API) and the [Official Google Gemini API](https://aistudio.google.com/) before using this package.
You can find most help on the [FAQ](https://github.com/dsdanielpark/Gemini-API/blob/main/documents/README_FAQ.md) and [Issue](https://github.com/dsdanielpark/Gemini-API/issues) pages. 


            
## [Issues](https://github.com/dsdanielpark/Gemini-API/issues)
Sincerely grateful for any reports on new features or bugs. Your valuable feedback on the code is highly appreciated. Frequent errors may occur due to changes in Google's service API interface. Both [Issue reports](https://github.com/dsdanielpark/Gemini-API/issues) and [Pull requests](https://github.com/dsdanielpark/Gemini-API/pulls) contributing to improvements are always welcome. We strive to maintain an active and courteous open community.


## Sponsor
Use [Crawlbase](https://crawlbase.com/) API for efficient data scraping to train AI models, boasting a 98% success rate and 99.9% uptime. It's quick to start, GDPR/CCPA compliant, supports massive data extraction, and is trusted by 70k+ developers.

## Contributors
We would like to express our sincere gratitude to all the contributors. 

This package aims to re-implement the functionality of the [Bard API](https://github.com/dsdanielpark/Bard-API/), which has been archived for the contributions of the beloved open-source community, despite Gemini's official API already being available.

Contributors to the [Bard API](https://github.com/dsdanielpark/Bard-API/) and [Gemini API](https://github.com/dsdanielpark/Gemini-API/).

<a href="https://github.com/dsdanielpark/Bard_API/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=dsdanielpark/Bard_API" />
</a>

<br>

<details><summary>Further development potential</summary>

Modifications to the async client using my logic are needed, along with automatic cookie collection via browser_cookie3, and implementation of other Bard API features (such as code extraction, export to Replit, graph drawing, etc.).

Please note that while reviewing automatic cookie collection, it appears that cookies expire immediately upon sending a request for collection. Efforts to make it more user-friendly were unsuccessful. Also, the _sid value seems to work normally even when returned as None.

Lastly, if the CustomParser and ResponseParser algorithms do not function properly, new parsing methods can be updated through conditional statements in the relevant sections.

I do not plan to actively curate this repository. Please review [HanaokaYuzu/Gemini-API](https://github.com/HanaokaYuzu/Gemini-API) first.

Thank you, and have a great day.
</details>

## Contacts

Core maintainers:
- [Antonio Cheong](https://github.com/acheong08) / teapotv8@proton.me <br>
- [Daniel Park](https://github.com/DSDanielPark) / parkminwoo1991@gmail.com
 


## License ©️ 
[MIT](https://opensource.org/license/mit/) license, 2024. We hereby strongly disclaim any explicit or implicit legal liability related to our works. Users are required to use this package responsibly and at their own risk. This project is a personal initiative and is not affiliated with or endorsed by Google. It is recommended to use Google's official API.


## References
[1] Github: [acheong08/Bard](https://github.com/acheong08/Bard) <br>
[2] GitHub: [HanaokaYuzu/Gemini-API](https://github.com/HanaokaYuzu/Gemini-API) <br>
[3] Github: [dsdanielpark/Bard-API](https://github.com/dsdanielpark/Bard-API) <br>
[4] Github: [GoogleCloudPlatform/generative-ai](https://github.com/GoogleCloudPlatform/generative-ai) <br>
[5] WebSite: [Google AI Studio](https://ai.google.dev/tutorials/ai-studio_quickstart) <br>

> *Warning*
Users assume full legal responsibility for GeminiAPI. Not endorsed by Google. Excessive use may lead to account restrictions. Changes in policies or account status may affect functionality. Utilize issue and discussion pages.

<br>

## Requirements
Python 3.7 or higher.

