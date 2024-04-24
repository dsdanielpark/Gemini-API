import aiohttp
import asyncio
from .const import FREE_MODELS
from typing import List, Optional


class AsyncOpenRouter:
    """
    Manages API interactions with OpenRouter for creating chat completions using AI models asynchronously.

    Attributes and methods are analogous to the synchronous version but adapted for async operation.
    """

    def __init__(self, model: str, api_key: str) -> None:
        if not api_key:
            raise ValueError(
                "API key required. Please visit https://openrouter.ai/keys"
            )
        self.api_key = api_key
        self.model = model
        self._validate_model(model)

    def get_model_list(self) -> List[str]:
        return self.FREE_MODEL_LIST

    async def create_chat_completion(
        self,
        message: str,
        site_url: Optional[str] = None,
        app_name: Optional[str] = None,
    ) -> str:
        response = await self.generate_content(message, site_url, app_name)
        return response["choices"][0]["message"]["content"]

    async def create_multi_chat_completions(
        self,
        messages: List[str],
        site_url: Optional[str] = None,
        app_name: Optional[str] = None,
    ) -> List[str]:
        tasks = [
            self.create_chat_completion(message, site_url, app_name)
            for message in messages
        ]
        results = await asyncio.gather(*tasks)
        return results

    async def generate_content(
        self,
        message: str,
        site_url: Optional[str] = None,
        app_name: Optional[str] = None,
    ) -> dict:
        self._validate_message(message)
        self._validate_model(self.model)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if site_url:
            headers["HTTP-Referer"] = site_url
        if app_name:
            headers["X-Title"] = app_name

        data = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": message},
            ],
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
            ) as response:
                response.raise_for_status()
                return await response.json()

    def _validate_message(self, message: str) -> None:
        if not isinstance(message, str):
            raise ValueError("Message must be a string")

    def _validate_model(self, model: str) -> None:
        """
        Checks if the specified model is in the list of free models.
        """
        if model not in FREE_MODELS:
            print(
                "This model may not be free. Please check the following list for costs.\nUsers are responsible for API costs. Visit https://openrouter.ai/docs#models"
            )
