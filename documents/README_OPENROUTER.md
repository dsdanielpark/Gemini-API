# OpenRouter: Free Open-Source LLMs API


OpenRouter offers free access to various open-source Large Language Models (LLMs), allowing you to explore and experiment with these powerful models without incurring any charges.

> [!IMPORTANT]
> The free models may be temporary and subject to change based on policies. Please refer to the following page to check the available free models: [Open Router Models](https://openrouter.ai/docs#models) (Free limit: 10 requests/minute)


<br>

## Installation
```
pip install python-gemini-api
```


## Quick Start
Get API key at [OpenRouter](https://openrouter.ai/keys) and generate contents as follow:
```python
from gemini import OpenRouter

api_key = "<your_api_key>"
gemma_client = OpenRouter(api_key=api_key, model="google/gemma-7b-it:free")

response = gemma_client.create_chat_completion("Do you know UCA academy in Korea?")
print(response)
```

> [!NOTE]
> You can easily receive responses from open LLMs without this package by following the instructions on [here](https://openrouter.ai/docs#models).


<br>

### Prerequisites

1. **Obtain an API Key**: Sign up for a free account on [OpenRouter](https://openrouter.ai/keys) and obtain your API key.

2. **Check Available Free Models**: OpenRouter provides a list of [free models](https://openrouter.ai/docs#models) that you can use. These models have a 0-dollar token cost, ensuring you won't be charged for their usage.


3. **Current Free Model List** (2024-03-27):
   - `google/gemma-7b-it:free` - [google/gemma-7b](https://huggingface.co/google/gemma-7b) from Google
   - `mistralai/mistral-7b-instruct:free` - [mistralai/Mistral-7B-v0.1](https://huggingface.co/mistralai/Mistral-7B-v0.1) from Mistral AI
   - `huggingfaceh4/zephyr-7b-beta:free` -[HuggingFaceH4/zephyr-7b-beta](https://huggingface.co/HuggingFaceH4/zephyr-7b-beta) 
   - `openchat/openchat-7b:free` - [openchat/openchat](https://huggingface.co/openchat/openchat) 
   - `openrouter/cinematika-7b:free` - [jondurbin/cinematika-7b-v0.1](https://huggingface.co/jondurbin/cinematika-7b-v0.1)
   - `undi95/toppy-m-7b:free` - [Undi95/Toppy-M-7B](https://huggingface.co/Undi95/Toppy-M-7B?not-for-all-audiences=true)
   - `gryphe/mythomist-7b:free` - [Gryphe/MythoMist-7b](https://huggingface.co/Gryphe/MythoMist-7b)
   - `nousresearch/nous-capybara-7b:free` - [NousResearch/Nous-Capybara-7B-V1](https://huggingface.co/NousResearch/Nous-Capybara-7B-V1) from Nous Research


> [!IMPORTANT]
> The free models may be temporary and subject to change based on policies. Please refer to the following page to check the available free models: [Open Router Models](https://openrouter.ai/docs#models)


<br>

## Usage Examples
Here are examples using some of the models. Simply change the model to use different ones.
> [!NOTE]
> Note that the availability and performance of these free models may vary over time. It's recommended to regularly check the OpenRouter documentation for the latest updates and information.


### google/gemma-7b-it:free


*chat completion*
```python
from gemini import OpenRouter

api_key = "<your_api_key>"
gemma_client = OpenRouter(api_key=api_key, model="google/gemma-7b-it:free")

prompt = "Do you know UCA academy in Korea?"
response = gemma_client.create_chat_completion(prompt)
print(response)
```

*get response*
```python
prompt = "Do you know UCA academy in Korea?"
payload = gemma_client.generate_content(prompt)
print(payload.json())
```


<br>

### mistralai/mistral-7b-instruct:free

```python

from gemini import OpenRouter

api_key = "<your_api_key>"
mistral_client = OpenRouter(api_key=api_key, model="mistralai/mistral-7b-instruct:free")

prompt = "Do you know UCA academy in Korea?"
response = mistral_client.create_chat_completion(prompt)
print(response)

# payload = mistral_client.generate_content(prompt)
# print(payload.json())

```

### openrouter/cinematika-7b:free

```python
from gemini import OpenRouter

api_key = "<your_api_key>"
cinematika_client = OpenRouter(api_key=api_key, model="openrouter/cinematika-7b:free")

prompt = "Write a brief synopsis for a sci-fi movie about time travel."
response = cinematika_client.create_chat_completion(prompt)
print(response)
```

### undi95/toppy-m-7b:free

```python
from gemini import OpenRouter

api_key = "<your_api_key>"
toppy_client = OpenRouter(api_key=api_key, model="undi95/toppy-m-7b:free")

prompt = "Give me infomation of Seoul, Korea."
response = toppy_client.create_chat_completion(prompt)
print(response)
```

### More Examples

Check out the [OpenRouter documentation](https://openrouter.ai/docs) for more examples and usage details for the other available free models.

