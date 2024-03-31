from typing import Dict, Any
from gemini.src.model.parser.base import BaesParser


class ParseMethod1(BaesParser):
    def parse(self, response_text: str) -> Dict[str, Any]:
        """
        Parses the given response text into a structured format.

        This method processes the input text by filtering and organizing its content based on specific criteria. It looks for items that start with certain prefixes or contain specific substrings, excluding items that are encrypted or represent images. The result is structured into a dictionary with keys for text and choices, where each choice includes a choice ID, text, and links.

        Args:
            response_text (str): The raw response text to be parsed.

        Returns:
            Dict[str, Any]: A dictionary containing the structured representation of the response text. This includes a general text field and fields for each choice found in the response, each with its own ID, text, and list of links.
        """
        response_items = response_text.lstrip("')]}'\n\n").split("\n")[1].split("\\")
        response_items = [item for item in response_items if item]
        processed_items = [
            x
            for x in response_items
            if x[0] == "n" or "https://" in x or "http://" in x or "rc_" in x
        ]
        processed_items = [
            x for x in processed_items if "encrypted" not in x and "[Image" not in x
        ]
        cleand_items = [
            item.lstrip("n").lstrip('"').replace("  ", " ") for item in processed_items
        ]
        cleand_items = [item for item in cleand_items if item]

        result = {"text": ""}
        choice_count = 0
        current_key = None

        for item in cleand_items:
            if item.startswith("rc_"):
                choice_count += 1
                current_key = f"choice{choice_count:02}"
                result[current_key] = {
                    "choice_id": item,
                    "text": "",
                    "links": [],
                }
            elif "http" in item and current_key:
                result[current_key]["links"].append(item)
            elif current_key:
                if result[current_key]["text"]:
                    result[current_key]["text"] += "\n" + item
                else:
                    result[current_key]["text"] = item
            else:
                if result["text"]:
                    result["text"] += "\n" + item
                else:
                    result["text"] = item

        if "choice01" in result:
            result["text"] = result["choice01"]["text"]

        parsed_response_text = {}
        for key in sorted(result.keys()):
            if key.startswith("choice"):
                sorted_choice = {
                    "choice_id": result[key]["choice_id"],
                    "text": result[key]["text"],
                    "links": result[key]["links"],
                }
                parsed_response_text[key] = sorted_choice
            else:
                parsed_response_text[key] = result[key]

        return parsed_response_text


class ParseMethod2(BaesParser):
    def parse(self, response_text: str) -> Dict[str, Any]:
        """
        Parses the given response text into a structured JSON-like format.

        This method initially processes the response string to extract items, focusing on those starting with 'n'. It then organizes these items into a JSON-like structure, grouping them into choices based on their keys and values. The method aims to restructure the response into a more readable and accessible format, with each choice assigned a unique key.

        Args:
            response_text (str): The raw response text to be parsed.

        Returns:
            Dict[str, Any]: A dictionary representing the structured version of the response text. This includes a series of choices, each with its own set of key-value pairs derived from the response. If a 'choice01' is present, its 'snippet' is also set as the main text of the response.
        """
        # Initial processing of the response string
        response_items = response_text.lstrip("')]}'\n\n").split("\n")[1].split("\\")
        response_items = [item for item in response_items if item]
        processed_items = [x for x in response_items if x[0] == "n"]

        # Extracting information into JSON format
        temp_dict = {}
        json_data = []
        for item in processed_items:
            key, value = item.split(": ", 1)
            if key == "nsnippet" and temp_dict:
                json_data.append(temp_dict)
                temp_dict = {}
            temp_dict[key] = value
        if temp_dict:
            json_data.append(temp_dict)

        # Restructuring the JSON data
        parsed_response_text = {}
        for index, item in enumerate(json_data, start=1):
            choice_key = f"choice{index:02}"
            choice_value = {}
            for key, value in item.items():
                new_key = key[1:]  # Remove the 'n' from the key
                choice_value[new_key] = value
            parsed_response_text[choice_key] = choice_value
        try:
            parsed_response_text["text"] = parsed_response_text["choice01"]["snippet"]
        except:
            pass
        return parsed_response_text
