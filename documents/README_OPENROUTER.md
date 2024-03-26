# OpenRouter: Free Open-Source LLMs API


OpenRouter offers free access to various open-source Large Language Models (LLMs), allowing you to explore and experiment with these powerful models without incurring any charges.


<br>

## Quick Start
Get API key at [OpenRouter](https://openrouter.ai/keys) and generate contents as follow:
```python
from gemini import OpenRouter

api_key = "<your_api_key>"
gemma_client = OpenRouter(api_key=api_key, model="google/gemma-7b-it:free")

response = gemma_client.create_chat_completion("Do you know UCA academy in Korea?")
print(response)
```

<br>

### Prerequisites

1. **Obtain an API Key**: Sign up for a free account on [OpenRouter](https://openrouter.ai/keys) and obtain your API key.

2. **Check Available Free Models**: OpenRouter provides a list of [free models](https://openrouter.ai/docs#models) that you can use. These models have a 0-dollar token cost, ensuring you won't be charged for their usage.


3. **Current Free Model List** (2024-03-26):
   - `google/gemma-7b-it:free` - 7B parameter Italian language model from Google
   - `openrouter/cinematika-7b:free` - 7B parameter multimodal model trained on movie data
   - `undi95/toppy-m-7b:free` - 7B parameter Korean language model
   - `gryphe/mythomist-7b:free` - 7B parameter model trained on mythology and fantasy texts
   - `mistralai/mistral-7b-instruct:free` - 7B parameter instructional model from Mistral AI
   - `nousresearch/nous-capybara-7b:free` - 7B parameter model from Nous Research
   - `openrouter/auto` - Automatic model selection based on input prompt

> [!IMPORTANT]
> The free models may be temporary and subject to change based on policies. Please refer to the following page to check the available free models: [Open Router Models](https://openrouter.ai/docs#models)


<br>

## Usage Examples
Here are examples using some of the models. Simply change the model to use different ones.
> [!NOTE]
> Note that the availability and performance of these free models may vary over time. It's recommended to regularly check the OpenRouter documentation for the latest updates and information.


### google/gemma-7b-it:free

```python
from gemini import OpenRouter

api_key = "<your_api_key>"
gemma_client = OpenRouter(api_key=api_key, model="google/gemma-7b-it:free")

prompt = "Do you know UCA academy in Korea?"
response = gemma_client.create_chat_completion(prompt)
print(response)
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
