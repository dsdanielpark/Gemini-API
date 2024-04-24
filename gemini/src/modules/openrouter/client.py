import requests
from .const import FREE_MODELS
from typing import List, Optional
from requests.models import Response


class OpenRouter:
    """
    Manages API interactions with OpenRouter for creating chat completions using AI models.

    Attributes:
        FREE_MODEL_LIST (List[str]): A list of free model identifiers available for use.
        api_key (str): The API key for authentication with OpenRouter services.
        model (str): The model identifier to be used for generating completions.

    Methods:
        __init__(model, api_key): Initializes the OpenRouter instance with a specified model and API key.
        create_chat_completion(message, site_url=None, app_name=None): Generates a chat completion for a given message.
        generate_content(message, site_url=None, app_name=None): Validates and sends a request to generate content.
        get_model_list(): Returns a list of free model identifiers available.

    Raises:
        ValueError: If an API key is not provided or if the message format is incorrect.
    """

    def __init__(self, model: str, api_key: str) -> None:
        """
        Initializes the OpenRouter instance with a specified model and API key.

        Parameters:
            model (str): The model identifier for generating chat completions.
            api_key (str): The API key for authentication.

        Raises:
            ValueError: If an API key is not provided.
        """
        self.api_key = api_key
        if not api_key:
            raise ValueError(
                "API key required. Please visit https://openrouter.ai/keys"
            )
        self.model = model
        self._validate_model(model)

    def get_model_list(self) -> List[str]:
        """
        Returns a list of free model identifiers available for use.
        """
        return self.FREE_MODEL_LIST

    def create_chat_completion(
        self,
        message: str,
        site_url: Optional[str] = None,
        app_name: Optional[str] = None,
    ) -> str:
        """
        Generates a chat completion for a given message.

        Parameters:
            message (str): The message for which to generate a completion.
            site_url (Optional[str], optional): The site URL to be included in the request headers.
            app_name (Optional[str], optional): The application name to be included in the request headers.

        Returns:
            str: The content of the first choice of the generated chat completion.
        """
        response = self.generate_content(message, site_url, app_name)
        return response.json()["choices"][0]["message"]["content"]

    def generate_content(
        self,
        message: str,
        site_url: Optional[str] = None,
        app_name: Optional[str] = None,
    ) -> Response:
        """
        Validates and sends a request to OpenRouter to generate content based on the provided message.

        Parameters:
            message (str): The message for which content generation is requested.
            site_url (Optional[str], optional): The site URL to be included in the request headers.
            app_name (Optional[str], optional): The application name to be included in the request headers.

        Returns:
            Response: The response object from the API request.
        """
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

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data
        )
        response.raise_for_status()

        return response

    def _validate_message(self, message: str) -> None:
        """
        Validates that the message is a string.
        """
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
