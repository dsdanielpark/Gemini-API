import random
import httpx
import asyncio
import datetime
import os
from pathlib import Path
from typing import List, Optional, Dict
from loguru import logger
from pydantic import BaseModel, HttpUrl


class GeminiImage(BaseModel):
    url: HttpUrl
    title: str = "[Image]"
    alt: str = ""

    @staticmethod
    def validate_images(images):
        if images == []:
            raise ValueError("Input is empty. Please provide images to proceed.")

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
            pass

    async def save(
        self,
        save_path: str = "cached",
        filename: Optional[str] = None,
        cookies: Optional[dict] = None,
    ) -> Optional[Path]:
        """
        Downloads the image from the URL and saves it to the specified save_path.

        Args:
            save_path: The directory to save the image (default: "cached").
            filename: The filename for the saved image (optional, uses title if not provided).
            cookies: Optional cookies dictionary for the download request.

        Returns:
            The save_path to the saved image file or None if download fails.
        """
        image_data = await self.fetch_bytes(self.url, cookies)
        GeminiImage.validate_images(image_data)
        now = datetime.datetime.now().strftime("%y%m%d%H%M%S")

        if not filename:
            filename = f"{self.title.replace(' ', '_').replace('[Image]', '').replace('/', '_').replace(':', '_')}_{random.randint(10,99)}_{now}.jpg"

        save_path = Path(save_path) / filename
        save_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            save_path.write_bytes(image_data)
            print(f"Saved {self.title} to {save_path}")
            return save_path
        except Exception as e:
            print(f"Failed to save image {self.title}: {str(e)}")
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
        GeminiImage.validate_images(images)
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
    async def save_images(
        image_data: Dict[str, bytes], save_path: str = "cached", unique: bool = True
    ):
        """Asynchronously saves images specified by their bytes data.

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
                print(f"Saved {title} to {save_path}")
            except:
                pass

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
