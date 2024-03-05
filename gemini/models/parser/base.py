from abc import ABC, abstractmethod


class ResponseParser(ABC):
    @abstractmethod
    def parse(self, response_text):
        pass

    @classmethod
    def add_custom_method(cls, method_name, function):
        setattr(cls, method_name, function)
