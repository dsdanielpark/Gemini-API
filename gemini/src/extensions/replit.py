import json


def prepare_replit_data(instructions: str, code: str, filename: str) -> list:
    """
    Creates and returns the input image data structure based on provided parameters.

    Args:
        instructions (str): The instruction text.
        code (str): The code.
        filename (str): The filename.

    Returns:
        list: The input image data structure.
    """
    return [
        [
            [
                "qACoKe",
                json.dumps([instructions, 5, code, [[filename, code]]]),
                None,
                "generic",
            ]
        ]
    ]
