import httpx
from pathlib import Path
from loguru import logger
from typing import List, Optional, Dict
from pydantic import BaseModel, HttpUrl


class GeminiImage(BaseModel):
    url: HttpUrl
    title: str = "[Image]"
    alt: str = ""

    def __str__(self):
        return f"{self.title}({self.url}) - {self.alt}"

    async def save(
        self,
        path: str = "temp",
        filename: Optional[str] = None,
        cookies: Optional[dict] = None,
    ) -> Optional[Path]:
        filename = filename or Path(self.url).name
        save_path = Path(path) / filename
        save_path.parent.mkdir(parents=True, exist_ok=True)

        async with httpx.AsyncClient(follow_redirects=True, cookies=cookies) as client:
            try:
                response = await client.get(self.url)
                response.raise_for_status()
                save_path.write_bytes(response.content)
                return save_path
            except httpx.HTTPStatusError as e:
                logger.error(
                    f"Error downloading image: {e.response.status_code} {e.response.reason_phrase}"
                )
                return None


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
