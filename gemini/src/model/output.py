import httpx
import asyncio
from pathlib import Path
from loguru import logger
from typing import List, Optional, Dict
from pydantic import BaseModel, HttpUrl


class GeminiImage(BaseModel):
    """A class for handling images from the Gemini API."""

    url: HttpUrl
    title: str = "[Image]"
    alt: str = ""

    async def save(
        self,
        path: str = "images",
        filename: Optional[str] = None,
        cookies: Optional[dict] = None,
    ) -> Optional[Path]:
        """Asynchronously saves the image to the specified path.

        Args:
            path (str): The directory where the image will be saved.
            filename (str, optional): The filename for the saved image. If not provided,
                a filename is generated based on the image title.
            cookies (dict, optional): Cookies to be used for downloading the image.

        Returns:
            Optional[Path]: The path where the image is saved, or None if saving fails.
        """
        bytes_data = await self.fetch_bytes(self.url, cookies)
        if bytes_data:
            filename = (
                filename
                or f"{self.title.replace(' ', '_').replace('[Image]', '').replace('/', '_').replace(':', '_')}.jpg"
            )
            save_path = Path(path) / filename
            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_path.write_bytes(bytes_data)
            return save_path

    @staticmethod
    async def fetch_bytes(
        url: HttpUrl, cookies: Optional[dict] = None
    ) -> Optional[bytes]:
        """Asynchronously fetches the bytes data of an image from the given URL.

        Args:
            url (str): The URL of the image.
            cookies (dict, optional): Cookies to be used for downloading the image.

        Returns:
            Optional[bytes]: The bytes data of the image, or None if fetching fails.
        """
        try:
            async with httpx.AsyncClient(
                follow_redirects=True, cookies=cookies
            ) as client:
                response = await client.get(url)
                response.raise_for_status()
                return response.content
        except Exception as e:
            print(f"Failed to download {url}: {str(e)}")
            return None

    @staticmethod
    async def fetch_images_dict(
        images: List["GeminiImage"], cookies: Optional[dict] = None
    ) -> Dict[str, bytes]:
        """Asynchronously fetches bytes data for a list of images.

        Args:
            images (List[GeminiImage]): A list of GeminiImage objects.
            cookies (dict, optional): Cookies to be used for downloading the images.

        Returns:
            Dict[str, bytes]: A dictionary mapping image titles to bytes data.
        """
        try:
            tasks = [image.fetch_bytes(image.url, cookies) for image in images]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return {
                images[i].title: result
                for i, result in enumerate(results)
                if isinstance(result, bytes)
            }
        except Exception as e:
            print(f"Error fetching images: {str(e)}")
            return {}

    @staticmethod
    async def save_images(image_data: Dict[str, bytes], path: str = "images"):
        """Asynchronously saves images specified by their bytes data.

        Args:
            image_data (Dict[str, bytes]): A dictionary mapping image titles to bytes data.
            path (str, optional): The directory where the images will be saved. Defaults to "images".
        """
        for title, data in image_data.items():
            filename = f"{title.replace(' ', '_').replace('[Image]', '').replace('/', '_').replace(':', '_')}.jpg"
            save_path = Path(path) / filename
            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_path.write_bytes(data)
            print(f"Saved {title} to {save_path}")

    def save_sync(
        self,
        path: str = "images",
        filename: Optional[str] = None,
        cookies: Optional[dict] = None,
    ) -> Optional[Path]:
        """Synchronously saves the image to the specified path.

        Args:
            path (str): The directory where the image will be saved.
            filename (str, optional): The filename for the saved image. If not provided,
                a filename is generated based on the image title.
            cookies (dict, optional): Cookies to be used for downloading the image.

        Returns:
            Optional[Path]: The path where the image is saved, or None if saving fails.
        """
        bytes_data = self.fetch_bytes_sync(self.url, cookies)
        if bytes_data:
            filename = (
                filename
                or f"{self.title.replace(' ', '_').replace('[Image]', '').replace('/', '_').replace(':', '_')}.jpg"
            )
            save_path = Path(path) / filename
            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_path.write_bytes(bytes_data)
            return save_path

    @staticmethod
    def fetch_bytes_sync(
        url: HttpUrl, cookies: Optional[dict] = None
    ) -> Optional[bytes]:
        """Synchronously fetches the bytes data of an image from the given URL.

        Args:
            url (str): The URL of the image.
            cookies (dict, optional): Cookies to be used for downloading the image.

        Returns:
            Optional[bytes]: The bytes data of the image, or None if fetching fails.
        """
        try:
            url_str = str(url)
            with httpx.Client(
                follow_redirects=True, max_redirects=10, cookies=cookies
            ) as client:
                response = client.get(url_str)
                response.raise_for_status()
                return response.content
        except Exception as e:
            print(f"Failed to download {url}: {str(e)}")
            return None

    @staticmethod
    def fetch_images_dict_sync(
        images: List["GeminiImage"], cookies: Optional[dict] = None
    ) -> Dict[str, bytes]:
        """Synchronously fetches bytes data for a list of images.

        Args:
            images (List[GeminiImage]): A list of GeminiImage objects.
            cookies (dict, optional): Cookies to be used for downloading the images.

        Returns:
            Dict[str, bytes]: A dictionary mapping image titles to bytes data.
        """
        results = [GeminiImage.fetch_bytes_sync(image.url, cookies) for image in images]
        return {images[i].title: result for i, result in enumerate(results) if result}

    @staticmethod
    def save_images_sync(image_data: Dict[str, bytes], path: str = "images"):
        """Synchronously saves images specified by their bytes data.

        Args:
            image_data (Dict[str, bytes]): A dictionary mapping image titles to bytes data.
            path (str, optional): The directory where the images will be saved. Defaults to "images".
        """
        for title, data in image_data.items():
            filename = f"{title.replace(' ', '_').replace('[Image]', '').replace('/', '_').replace(':', '_')}.jpg"
            save_path = Path(path) / filename
            save_path.parent.mkdir(parents=True, exist_ok=True)


class GeminiCandidate(BaseModel):
    """A class representing a candidate returned by the Gemini model."""

    rcid: str
    text: str
    web_images: List[GeminiImage] = []
    generated_images: List[GeminiImage] = []
    response_dict: Dict = {}


class GeminiModelOutput(BaseModel):
    """A class representing the output of the Gemini model."""

    metadata: List[str]
    candidates: List[GeminiCandidate]
    chosen: int = 0
    response_dict: Optional[dict] = None

    @property
    def rcid(self) -> str:
        """The RCID (Reversed-Cloze ID) of the chosen candidate."""
        return self.candidates[self.chosen].rcid

    @property
    def text(self) -> str:
        """The text of the chosen candidate."""
        return self.candidates[self.chosen].text

    @property
    def web_images(self) -> List[GeminiImage]:
        """A list of web images associated with the chosen candidate."""
        return self.candidates[self.chosen].web_images

    @property
    def generated_images(self) -> List[GeminiImage]:
        """A list of generated images associated with the chosen candidate."""
        return self.candidates[self.chosen].generated_images

    @property
    def response_dict(self) -> Optional[Dict]:
        """The response dictionary associated with the model output."""
        return self.response_dict
