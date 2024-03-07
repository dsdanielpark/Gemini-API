import httpx
import asyncio
from pathlib import Path
from loguru import logger
from typing import List, Optional, Dict
from pydantic import BaseModel, HttpUrl


class GeminiImage(BaseModel):
    url: HttpUrl
    title: str = "[Image]"
    alt: str = ""

    @staticmethod
    async def fetch_bytes(
        url: HttpUrl, cookies: Optional[dict] = None
    ) -> Optional[bytes]:
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

    async def save(
        self,
        path: str = "images",
        filename: Optional[str] = None,
        cookies: Optional[dict] = None,
    ) -> Optional[Path]:
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
    async def fetch_images_dict(
        images: List["GeminiImage"], cookies: Optional[dict] = None
    ) -> Dict[str, bytes]:
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
        for title, data in image_data.items():
            filename = f"{title.replace(' ', '_').replace('[Image]', '').replace('/', '_').replace(':', '_')}.jpg"
            save_path = Path(path) / filename
            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_path.write_bytes(data)
            print(f"Saved {title} to {save_path}")

    @staticmethod
    def fetch_bytes_sync(
        url: HttpUrl, cookies: Optional[dict] = None
    ) -> Optional[bytes]:
        try:
            url_str = str(url)
            with httpx.Client(follow_redirects=True, cookies=cookies) as client:
                response = client.get(url_str)
                response.raise_for_status()
                return response.content
        except Exception as e:
            print(f"Failed to download {url}: {str(e)}")
            return None

    def save_sync(
        self,
        path: str = "images",
        filename: Optional[str] = None,
        cookies: Optional[dict] = None,
    ) -> Optional[Path]:
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
    def fetch_images_dict_sync(
        images: List["GeminiImage"], cookies: Optional[dict] = None
    ) -> Dict[str, bytes]:
        results = [GeminiImage.fetch_bytes_sync(image.url, cookies) for image in images]
        return {images[i].title: result for i, result in enumerate(results) if result}

    @staticmethod
    def save_images_sync(image_data: Dict[str, bytes], path: str = "images"):
        for title, data in image_data.items():
            filename = f"{title.replace(' ', '_').replace('[Image]', '').replace('/', '_').replace(':', '_')}.jpg"
            save_path = Path(path) / filename
            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_path.write_bytes(data)
            print(f"Saved {title} to {save_path}")


class GeminiCandidate(BaseModel):
    rcid: str
    text: str
    web_images: List[GeminiImage] = []
    generated_images: List[GeminiImage] = []
    response_dict: Dict = {}


class GeminiModelOutput(BaseModel):
    metadata: List[str]
    candidates: List[GeminiCandidate]
    chosen: int = 0
    response_dict: Optional[dict] = None

    @property
    def rcid(self) -> str:
        return self.candidates[self.chosen].rcid

    @property
    def text(self) -> str:
        return self.candidates[self.chosen].text

    @property
    def web_images(self) -> List[GeminiImage]:
        return self.candidates[self.chosen].web_images

    @property
    def generated_images(self) -> List[GeminiImage]:
        return self.candidates[self.chosen].generated_images

    @property
    def response_dict(self) -> Optional[Dict]:
        return self.response_dict
