from gemini.models.parser.base import ResponseParser

class ParseMethod1(ResponseParser):
    def parse(self, response_text):
        response_items = response_text.lstrip("')]}\'\n\n").split("\n")[1].split("\\")
        response_items = [item for item in response_items if item]
        processed_items = [x for x in response_items if x[0] == "n" or "https://" in x or "http://" in x or "rc_" in x]
        processed_items = [x for x in processed_items if "encrypted" not in x and "[Image" not in x]
        cleand_items = [item.lstrip('n').lstrip('"').replace("  ", " ") for item in processed_items]
        cleand_items = [item for item in cleand_items if item]

        json_data = {"text": ""}
        choice_count = 0
        current_key = None

        for item in cleand_items:
            if item.startswith('rc_'):
                choice_count += 1
                current_key = f'choice{choice_count:02}'
                json_data[current_key] = {"choice_id": item, "text": "", "links": []} 
            elif 'http' in item and current_key:
                json_data[current_key]["links"].append(item)
            elif current_key:
                if json_data[current_key]["text"]:
                    json_data[current_key]["text"] += "\n" + item
                else:
                    json_data[current_key]["text"] = item
            else:  
                if json_data["text"]:
                    json_data["text"] += "\n" + item
                else:
                    json_data["text"] = item

        if 'choice01' in json_data:
            json_data['text'] = json_data['choice01']['text']

        restructured_data = {}
        for key in sorted(json_data.keys()):
            if key.startswith('choice'):
                sorted_choice = {"choice_id": json_data[key]["choice_id"], "text": json_data[key]["text"], "links": json_data[key]["links"]}
                restructured_data[key] = sorted_choice
            else:
                restructured_data[key] = json_data[key]

        return restructured_data