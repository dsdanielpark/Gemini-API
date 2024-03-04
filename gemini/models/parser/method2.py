from gemini.models.parser.base import ResponseParser

class ParseMethod2(ResponseParser):
    def parse(self, response_text):
        # Initial processing of the response string
        response_items = response_text.lstrip("')]}\'\n\n").split("\n")[1].split("\\")
        response_items = [item for item in response_items if item]
        processed_items = [x for x in response_items if x[0] == "n"]

        # Extracting information into JSON format
        temp_dict = {}
        json_data = []
        for item in processed_items:
            key, value = item.split(": ", 1)
            if key == 'nsnippet' and temp_dict:
                json_data.append(temp_dict)
                temp_dict = {}
            temp_dict[key] = value
        if temp_dict:
            json_data.append(temp_dict)

        # Restructuring the JSON data
        restructured_data = {}
        for index, item in enumerate(json_data, start=1):
            choice_key = f'choice{index:02}'
            choice_value = {}
            for key, value in item.items():
                new_key = key[1:]  # Remove the 'n' from the key
                choice_value[new_key] = value
            restructured_data[choice_key] = choice_value
        try:
            restructured_data['text'] = restructured_data['choice01']['snippet']
        except:
            pass                               
        return restructured_data

