import argparse
from pydantic import HttpUrl
from ..gemini import GeminiImage


def parse_args():
    parser = argparse.ArgumentParser(
        description="Test the GeminiImage class functionality"
    )
    parser.add_argument(
        "--url",
        type=str,
        required=True,
        help="URL of the image to test",
        default="https://upload.wikimedia.org/wikipedia/commons/c/cf/Harvard_Yard_in_autumn%2C_Boston%2C_Massachusetts%2C_2015.jpg",
    )
    parser.add_argument(
        "--title", type=str, default="[Image]", help="Title of the image"
    )
    parser.add_argument(
        "--save_path", type=str, default="cached", help="Directory to save the images"
    )
    parser.add_argument(
        "--async", action="store_true", help="Use asynchronous methods for testing"
    )
    return parser.parse_args()


async def test_async(url, title, save_path, cookies):
    images = [GeminiImage(url=HttpUrl(url), title=title)]
    await GeminiImage.save(images, save_path, cookies)


def test_sync(url, title, save_path, cookies):
    images = [GeminiImage(url=HttpUrl(url), title=title)]
    GeminiImage.save_sync(images, cookies, save_path)


if __name__ == "__main__":
    args = parse_args()

    test_sync(args.url, args.title, args.save_path)
    test_async(args.url, args.title, args.save_path)
