# OpenRouter: Free Open-Source LLMs API

OpenRouter offers free access to various open-source Large Language Models (LLMs), allowing you to explore and experiment with these powerful models without incurring any charges. After contacting Open Route via Discord, they have confirmed that there are no plans to switch the free models to paid ones for the time being. (2024-04)

> [!IMPORTANT]
> The free models may be temporary and subject to change based on policies. Please refer to the following page to check the available free models: [Open Router Models](https://openrouter.ai/docs#models) (Free limit: 10 requests/minute)

## Features

- **Asynchronous API Calls**: Makes use of Python's `asyncio` and `aiohttp` to perform asynchronous API calls.
- **Concurrent Completions**: Ability to handle multiple chat completions concurrently.
- **Error Handling**: Basic error handling for API keys and message formatting.

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


<br><br><br>

# OpenRouter Async API Client

For the Gemini API, due to issues like rate limiting and blocking, sync objects are preferred over async, as async can be easily neutralized. However, since OpenRouter reliably provides open-source LLMs, you can use the asynchronous implementation as follows.

The `OpenRouter` class is designed to manage API interactions with OpenRouter for creating chat completions using AI models asynchronously. This class utilizes `aiohttp` for asynchronous network calls.

<br>

## Usage

### Initialization

Initialize an instance of `OpenRouter` with your model identifier and API key:

```python
from gemini import AsyncOpenRouter

api_key = 'your_api_key_here'
model = 'google/gemma-7b-it:free'
router = AsyncOpenRouter(model, api_key)
```

### Single Chat Completion

To generate a single chat completion asynchronously:

```python
import asyncio

async def main():
    completion = await router.create_chat_completion("Give me infomation of Seoul, Korea.")
    print(completion)

if __name__ == "__main__":
    asyncio.run(main())
```

```python
from gemini import AsyncOpenRouter

payload = await GemmaClient.create_chat_completion("Give me infomation of Seoul, Korea.")
```

### Multiple Chat Completions

To handle multiple chat completions concurrently:

```python
import asyncio

async def main():
    messages = [
        ""Give me infomation of Seoul, Korea.",
        "What is the weather like today?",
        "Can you recommend some books?"
    ]
    completions = await GemmaClient.create_multi_chat_completions(messages)
    for completion in completions:
        print(completion)

if __name__ == "__main__":
    asyncio.run(main())
```

```python
messages = [
        "Give me infomation of Seoul, Korea.",
        "What is the weather like today?",
        "Can you recommend some books?"
    ]

completions = await GemmaClient.create_multi_chat_completions(messages)

# Print completions
for completion in completions:
    print("-"*20)
    print(completion)
```

### Generate Content

To generate a single chat completion asynchronously:

```python
import asyncio

async def main():
    completion = await router.generate_content("Give me infomation of Seoul, Korea.")
    print(completion)

if __name__ == "__main__":
    asyncio.run(main())
```

```python
from gemini import AsyncOpenRouter

payload = await GemmaClient.generate_content("Give me infomation of Seoul, Korea.")
```

### More Examples

Check out the [OpenRouter documentation](https://openrouter.ai/docs) for more examples and usage details for the other available free models.

