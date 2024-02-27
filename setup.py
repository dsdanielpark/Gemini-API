import re
from setuptools import find_packages, setup


def read(file_path, version=False):
    with open(file_path, encoding="UTF-8") as f:
        content = f.read()
    if version:
        match = re.search(r"""^__version__ = ['"]([^'"]*)['"]""", content, re.M)
        if not match:
            raise RuntimeError(f"{file_path} doesn't contain __version__")
        return match.group(1)
    return content


setup(
    name="python-gemini-api",
    version=read("gemini/__init__.py", version=True),
    author="Daniel Park",
    author_email="parkminwoo1991@gmail.com",
    description="The python package that returns Response of Google Gemini through API.",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/dsdanielpark/Gemini-API",
    packages=find_packages(exclude=[]),
    python_requires=">=3.9",
    install_requires=[
        "httpx[http2]>=0.20.0",
        "requests",
        "colorama",
        "browser_cookie3",
        "loguru",
        "pydantic",
    ],
    extras_require={
        "translate": [
            "deep_translator",
            "google-cloud-translate",
            "langdetect",
        ]
    },
    keywords="Python, API, Gemini, Google Gemini, Large Language Model, Chatbot API, Google API, Chatbot",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    entry_points={"console_scripts": ["gemini=gemini.cli:main"]},
)
