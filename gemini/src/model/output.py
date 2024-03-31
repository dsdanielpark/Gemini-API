from pydantic import BaseModel
from typing import List, Optional, Dict
from gemini.src.model.image import GeminiImage


class GeminiCandidate(BaseModel):
    """A class representing a candidate returned by the Gemini model."""

    rcid: str
    text: str
    code: Dict = {}
    web_images: List[GeminiImage] = []
    generated_images: List[GeminiImage] = []
    response_dict: Dict = {}


class GeminiModelOutput(BaseModel):
    """A class representing the output of the Gemini model."""

    metadata: List[str]
    candidates: List[GeminiCandidate]
    chosen: int = 0
    response_dict: Optional[dict] = None

    def __setattr__(self, name, value):
        if name == "chosen":
            super().__setattr__(name, value)
        else:
            super().__setattr__(name, value)

    @property
    def rcid(self) -> str:
        """The rcid(response candidate id) of the chosen candidate."""
        return self.candidates[self.chosen].rcid

    @property
    def text(self) -> str:
        """The code of the chosen candidate."""
        return self.candidates[self.chosen].text

    @property
    def code(self) -> Optional[Dict]:
        """The text of the chosen candidate."""
        return self.candidates[self.chosen].code

    @property
    def web_images(self) -> List[GeminiImage]:
        """A list of web images associated with the chosen candidate."""
        return self.candidates[self.chosen].web_images

    @property
    def generated_images(self) -> List[GeminiImage]:
        """A list of generated images associated with the chosen candidate."""
        return self.candidates[self.chosen].generated_images

    @property
    def payload(self) -> Optional[Dict]:
        """The response dictionary associated with the model output."""
        return self.response_dict
