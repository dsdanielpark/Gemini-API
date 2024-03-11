from gemini.src.parser.base import BaesParser
import json


class ResponseParser(BaesParser):
    def __init__(self, cookies):
        self.cookies = cookies

    def parse(self, response_text):
        return self.parse_response_text(response_text)

    def parse_response_text(self, response_text):
        body = self._extract_body(response_text)

        if not body or not body[4]:
            raise ValueError(
                "Failed to parse response body. Data structure is invalid."
            )

        candidates = self._parse_candidates(body[4])
        metadata = body[1]

        if body[0] is None:
            prompt_class = None
            prompt_candidates = []
        else:
            prompt_class = body[0][0]
            prompt_candidates = body[0][1:] if len(body[0]) > 1 else []

        if not candidates:
            raise ValueError(
                "Failed to generate contents. No output data found in response."
            )

        return {
            "metadata": metadata,
            "prompt_class": prompt_class,
            "prompt_candidates": prompt_candidates,
            "candidates": candidates,
        }

    def _extract_body(self, response_text):
        try:
            body = json.loads(
                json.loads(response_text.lstrip("')]}'\n\n").split("\n")[1])[0][2]
            )
            if not body[4]:
                body = json.loads(
                    json.loads(response_text.lstrip("')]}'\n\n").split("\n")[1])[4][2]
                )
            return body
        except:
            try:
                body = json.loads(json.loads(response_text.text.split("\n")[2])[0][2])
                if not body[4]:
                    body = json.loads(
                        json.loads(response_text.text.split("\n")[2])[4][2]
                    )
                else:
                    raise ValueError(
                        "Failed to generate contents. Invalid response data received."
                    )
                return body
            except:
                max_response = max(response_text.split("\n"), key=len)
                body = json.loads(json.loads(max_response)[0][2])
                if not body[4]:
                    body = json.loads(json.loads(max_response)[4][2])
                return body

    def _parse_candidates(self, candidates_data):
        candidates_list = []
        for candidate_data in candidates_data:
            web_images = self._parse_web_images(candidate_data[4])
            generated_images = self._parse_generated_images(candidate_data[12])
            candidate_dict = {
                "rcid": candidate_data[0],
                "text": candidate_data[1][0],
                "web_images": web_images,
                "generated_images": generated_images,
            }
            candidates_list.append(candidate_dict)
        return candidates_list

    def _parse_web_images(self, images_data):
        if not images_data:
            return []
        return [
            {
                "url": image[0][0][0],
                "title": image[2],
                "alt": image[0][4],
            }
            for image in images_data
        ]

    def _parse_generated_images(self, images_data):
        if not images_data or not images_data[7] or not images_data[7][0]:
            return []
        return [
            {
                "url": image[0][3][3],
                "title": f"[GeneratedImage {image[3][6]}]",
                "alt": image[3][5][i] if len(image[3][5]) > i else image[3][5][0],
                "cookies": self.cookies,
            }
            for i, image in enumerate(images_data[7][0])
        ]
