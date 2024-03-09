import os
import random
import httpx
import asyncio
import datetime
from pathlib import Path
from typing import List, Optional, Dict
from loguru import logger
from pydantic import BaseModel, HttpUrl


class GeminiImage(BaseModel):
    url: HttpUrl
    title: str = "[Image]"
    alt: str = ""

    @classmethod
    def validate_images(cls, images):
        if not images:
            raise ValueError("Input is empty. Please provide images to proceed.")

    @staticmethod
    async def fetch_bytes(url: HttpUrl) -> Optional[bytes]:
        try:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                response = await client.get(str(url))
                response.raise_for_status()
                return response.content
        except Exception as e:
            print(f"Failed to download {url}: {str(e)}")
            return None

    @classmethod
    async def save(
        cls, images: List["GeminiImage"], save_path: str = "cached"
    ) -> Optional[Path]:
        cls.validate_images(images)
        image_data = await cls.fetch_images_dict(images)
        await cls.save_images(image_data, save_path)

    @classmethod
    async def fetch_images_dict(cls, images: List["GeminiImage"]) -> Dict[str, bytes]:
        cls.validate_images(images)
        tasks = [cls.fetch_bytes(image.url) for image in images]
        results = await asyncio.gather(*tasks)
        return {image.title: result for image, result in zip(images, results) if result}

    @staticmethod
    async def save_images(image_data: Dict[str, bytes], save_path: str = "cached"):
        os.makedirs(save_path, exist_ok=True)
        for title, data in image_data.items():
            now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
            filename = f"{title.replace(' ', '_')}_{now}.jpg"
            filepath = Path(save_path) / filename
            try:
                with open(filepath, "wb") as f:
                    f.write(data)
                print(f"Saved {title} to {filepath}")
            except Exception as e:
                print(f"Error saving {title}: {str(e)}")

    @staticmethod
    def fetch_bytes_sync(url: HttpUrl) -> Optional[bytes]:
        """Synchronously fetches the bytes data of an image from the given URL.

        Args:
            url (str): The URL of the image.

        Returns:
            Optional[bytes]: The bytes data of the image, or None if fetching fails.
        """
        try:
            with httpx.Client(follow_redirects=True) as client:
                response = client.get(str(url))
                response.raise_for_status()
                return response.content
        except Exception as e:
            print(f"Failed to download {url}: {str(e)}")
            return None

    @staticmethod
    def fetch_bytes_sync(
        url: HttpUrl, cookies: Optional[dict] = None
    ) -> Optional[bytes]:
        try:
            url_str = str(url)
            with httpx.Client(follow_redirects=True, cookies=cookies) as client:
                try:
                    response = client.get(url_str)
                except:
                    response = client.get(url)
                response.raise_for_status()
                return response.content
        except Exception as e:
            print(f"Failed to download {url}: {str(e)}")
            pass

    @staticmethod
    def save_sync(
        images: List["GeminiImage"],
        cookies: Optional[dict] = None,
        save_path: str = "cached",
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
        image_data = GeminiImage.fetch_images_dict_sync(images, cookies)
        GeminiImage.validate_images(image_data)
        GeminiImage.save_images_sync(image_data, save_path)

    @staticmethod
    def fetch_images_dict_sync(
        images: List["GeminiImage"], cookies: Optional[dict] = None
    ) -> Dict[str, bytes]:
        """Synchronously fetches the bytes data of an image from the given URL.

        Args:
            url (str): The URL of the image.
            cookies (dict, optional): Cookies to be used for downloading the image.

        Returns:
            Optional[bytes]: The bytes data of the image, or None if fetching fails.
        """
        GeminiImage.validate_images(images)
        results = [GeminiImage.fetch_bytes_sync(image.url, cookies) for image in images]
        return {images[i].title: result for i, result in enumerate(results) if result}

    @staticmethod
    def save_images_sync(
        image_data: Dict[str, bytes],
        save_path: str = "cached",
        unique: bool = True,
    ):
        """Synchronously saves images specified by their bytes data.

        Args:
            image_data (Dict[str, bytes]): A dictionary mapping image titles to bytes data.
            path (str, optional): The directory where the images will be saved. Defaults to "images".
        """
        os.makedirs(save_path, exist_ok=True)
        if unique:
            titles = set(image_data.keys())
            image_data = {
                title: data for title, data in image_data.items() if title in titles
            }
        for title, data in image_data.items():
            now = datetime.datetime.now().strftime("%y%m%d%H%M%S%f")
            filename = f"{title.replace(' ', '_').replace('[Image]', '').replace('/', '_').replace(':', '_')}_{random.randint(10,99)}_{now}.jpg"
            filepath = Path(save_path) / filename
            try:
                filepath.write_bytes(data)
            except:
                pass
            print(f"Saved {title} to {save_path}")
