import asyncio
import httpx
from typing import List, Dict, Optional
from pydantic import BaseModel, HttpUrl
from pathlib import Path


class GeminiImage(BaseModel):
    url: HttpUrl
    title: str = "[Image]"
    alt: str = ""

    def __str__(self):
        return f"{self.title}({self.url}) - {self.alt}"

    @staticmethod
    async def fetch_bytes(
        url: HttpUrl, cookies: Optional[dict] = None
    ) -> Optional[bytes]:
        async with httpx.AsyncClient(follow_redirects=True, cookies=cookies) as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                return response.content
            except httpx.RequestError as e:
                print(f"Request error: {e}")
                return None
            except httpx.HTTPStatusError as e:
                print(
                    f"HTTP error: {e.response.status_code} {e.response.reason_phrase}"
                )
                return None

    async def save(
        self,
        path: str = "images",
        filename: Optional[str] = None,
        cookies: Optional[dict] = None,
    ) -> Optional[Path]:
        bytes_data = await self.fetch_bytes(self.url, cookies)
        if bytes_data:
            filename = filename or Path(self.url).name
            save_path = Path(path) / filename
            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_path.write_bytes(bytes_data)
            return save_path
        else:
            return None

    @staticmethod
    async def fetch_images_as_bytes(
        images: List["GeminiImage"],
    ) -> Dict[str, Optional[bytes]]:
        tasks = [GeminiImage.fetch_bytes(image.url) for image in images]
        results = await asyncio.gather(*tasks)
        return {images[i].title: results[i] for i in range(len(images)) if results[i]}
