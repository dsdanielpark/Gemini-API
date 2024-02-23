from gemini.core import Gemini
from models.base import GeminiOutput
from typing import Optional, Any


class GeminiSession:
    """
    Chat data to retrieve conversation history. Only if all 3 ids are provided will the conversation history be retrieved.

    Parameters
    ----------
    gemini: `Gemini`
        Gemini client interface for https://gemini.google.com/
    metadata: `list[str]`, optional
        List of chat metadata `[cid, rid, rcid]`, can be shorter than 3 elements, like `[cid, rid]` or `[cid]` only
    cid: `str`, optional
        Chat id, if provided together with metadata, will override the first value in it
    rid: `str`, optional
        Reply id, if provided together with metadata, will override the second value in it
    rcid: `str`, optional
        Reply candidate id, if provided together with metadata, will override the third value in it
    """

    # @properties needn't have their slots pre-defined
    __slots__ = ["__metadata", "gemini", "output"]

    def __init__(
        self,
        gemini: Gemini,
        metadata: Optional[list[str]] = None,
        cid: Optional[str] = None,  # chat id
        rid: Optional[str] = None,  # reply id
        rcid: Optional[str] = None,  # reply candidate id
    ):
        self.__metadata: list[Optional[str]] = [None, None, None]
        self.gemini: Gemini = gemini
        self.output: Optional[GeminiOutput] = None

        if metadata:
            self.metadata = metadata
        if cid:
            self.cid = cid
        if rid:
            self.rid = rid
        if rcid:
            self.rcid = rcid

    def __str__(self):
        return f"GeminiSession(cid='{self.cid}', rid='{self.rid}', rcid='{self.rcid}')"

    __repr__ = __str__

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        if name == "output" and isinstance(value, GeminiOutput):
            self.metadata = value.metadata
            self.rcid = value.rcid

    def send_message(self, prompt: str) -> GeminiOutput:
        """
        Generates contents with prompt.
        Use as a shortcut for `Gemini.generate_content(prompt, self)`.

        Parameters
        ----------
        prompt: `str`
            Prompt provided by user

        Returns
        -------
        :class:`GeminiOutput`
            Output data from gemini.google.com, use `GeminiOutput.text` to get the default text reply, `GeminiOutput.images` to get a list
            of images in the default reply, `GeminiOutput.candidates` to get a list of all answer candidates in the output
        """
        return self.gemini.generate_content(prompt, self)

    def choose_candidate(self, index: int) -> GeminiOutput:
        """
        Choose a candidate from the last `GeminiOutput` to control the ongoing conversation flow.

        Parameters
        ----------
        index: `int`
            Index of the candidate to choose, starting from 0
        """
        if not self.output:
            raise ValueError("No previous output data found in this chat session.")

        if index >= len(self.output.candidates):
            raise ValueError(
                f"Index {index} exceeds the number of candidates in last model output."
            )

        self.output.chosen = index
        self.rcid = self.output.rcid
        return self.output

    @property
    def metadata(self):
        return self.__metadata

    @metadata.setter
    def metadata(self, value: list[str]):
        if len(value) > 3:
            raise ValueError("metadata cannot exceed 3 elements")
        self.__metadata[: len(value)] = value

    @property
    def cid(self):
        return self.__metadata[0]

    @cid.setter
    def cid(self, value: str):
        self.__metadata[0] = value

    @property
    def rid(self):
        return self.__metadata[1]

    @rid.setter
    def rid(self, value: str):
        self.__metadata[1] = value

    @property
    def rcid(self):
        return self.__metadata[2]

    @rcid.setter
    def rcid(self, value: str):
        self.__metadata[2] = value
