from typing import List, Optional, Dict

from gemini.src.tools.citation import DraftCitation
from gemini.src.tools.google.code import CodeContent
from gemini.src.tools.google.flight import BardFlightContent
from gemini.src.tools.google.gworkspace import GoogleWorkspaceContent
from gemini.src.tools.image import BardImageContent
from gemini.src.tools.google.hotel import BardHotelContent
from gemini.src.tools.google.json import JsonContent
from gemini.src.tools.google.link import BardLink
from gemini.src.tools.google.map import BardMapContent
from gemini.src.tools.google.tool_declaimer import BardToolDeclaimer
from gemini.src.tools.user_content import UserContent
from gemini.src.tools.google.youtube import BardYoutubeContent


class GeminiDraft:
    def __init__(self, input_list: list):
        self._input_list = input_list
        self.id = self._input_list[0]

    @property
    def text(self) -> str:
        return self._input_list[1][0]

    @property
    def text_with_user_content(self) -> str:
        text = self.text
        for uc in self.user_content.values():
            key = uc.key
            mk = uc.markdown_text
            text = text.replace(key, "\n" + mk)
        return text

    @property
    def citations(self) -> List[DraftCitation]:
        text = self.text
        return (
            [DraftCitation(c, text) for c in self._input_list[2][0]]
            if self._input_list[2]
            else []
        )

    @property
    def images(self) -> List[BardImageContent]:
        # also in self._attachments[1]
        return (
            [BardImageContent(img) for img in self._input_list[4]]
            if self._input_list[4]
            else []
        )

    @property
    def language(self) -> str:
        # en
        return self._input_list[9]

    @property
    def _attachments(self) -> Optional[list]:
        return self._input_list[12]

    @property
    def map_content(self) -> List[BardMapContent]:
        if not self._attachments:
            return []
        return (
            [BardMapContent(a) for a in self._attachments[3]]
            if self._attachments[3]
            else []
        )

    @property
    def json_content(self) -> List[JsonContent]:
        if not self._attachments:
            return []
        return (
            [JsonContent(a) for a in self._attachments[10]]
            if self._attachments[10]
            else []
        )

    @property
    def gworkspace(self) -> List[GoogleWorkspaceContent]:
        if not self._attachments or len(self._attachments) < 13:
            return []
        return (
            [GoogleWorkspaceContent(a) for a in self._attachments[12][0][2]]
            if self._attachments[12]
            else []
        )

    @property
    def youtube(self) -> List[BardYoutubeContent]:
        if not self._attachments:
            return []
        return (
            [BardYoutubeContent(a) for a in self._attachments[4]]
            if self._attachments[4]
            else []
        )

    @property
    def python_code(self) -> List[CodeContent]:
        # Google has a dedicated Python model that can also run code.
        # The text model uses the output of the Python model to generate answers,
        # including answers in other languages.
        #
        # The code snippet is the same for all drafts!
        if not self._attachments:
            return []
        return (
            [CodeContent(a) for a in self._attachments[5]]
            if self._attachments[5] and self._attachments[5][0][3]
            else []
        )

    @property
    def links(self) -> List[BardLink]:
        if not self._attachments:
            return []
        return (
            [BardLink(a) for a in self._attachments[8]] if self._attachments[8] else []
        )

    @property
    def flights(self) -> List[BardFlightContent]:
        if not self._attachments or len(self._attachments) < 17:
            return []
        return (
            [BardFlightContent(a) for a in self._attachments[16]]
            if self._attachments[16]
            else []
        )

    @property
    def hotels(self) -> List[BardHotelContent]:
        if not self._attachments or len(self._attachments) < 19:
            return []
        return (
            [BardHotelContent(a) for a in self._attachments[17]]
            if self._attachments[17]
            else []
        )

    @property
    def tool_disclaimers(self) -> List[BardToolDeclaimer]:
        if not self._attachments or len(self._attachments) < 23:
            return []

        return (
            [BardToolDeclaimer(a) for a in self._attachments[22]]
            if self._attachments[22]
            else []
        )

    @property
    def user_content(self) -> Dict[str, UserContent]:
        d = {v.key: v for v in self.youtube}
        d.update({v.key: v for v in self.map_content})
        d.update({v.key: v for v in self.flights})
        d.update({v.key: v for v in self.links})
        d.update({v.key: v for v in self.tool_disclaimers})
        d.update({v.key: v for v in self.json_content})
        d.update({v.key: v for v in self.hotels})
        return d

    def __str__(self) -> str:
        return self.text
