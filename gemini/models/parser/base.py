from abc import ABC, abstractmethod


class BaesParser(ABC):
    """
    An abstract base class for response parsers.

    This class provides a structure for parsing responses from various sources. It requires the implementation of a `parse` method for processing response text. Additionally, it allows the dynamic addition of custom methods to parser classes.
    """

    @abstractmethod
    def parse(self, response_text: str) -> any:
        """
        Parses the given response text.

        This method must be implemented by subclasses to define specific parsing behavior.

        Args:
            response_text (str): The text of the response to be parsed.

        Returns:
            The parsed data, format depends on the implementation.
        """
        pass

    @classmethod
    def add_custom_method(cls, method_name: str, function: callable):
        """
        Dynamically adds a custom method to the parser class.

        This allows for extending the functionality of parser instances at runtime.

        Args:
            method_name (str): The name of the method to be added.
            function (callable): The function to be set as a method of the class.
        """
        # Recommend to start from this codes
        # response_items = response_text.lstrip("')]}\'\n\n").split("\n")[1].split("\\")
        # response_items = [item for item in response_items if item]
        setattr(cls, method_name, function)
