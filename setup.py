# Copyright 2024 Daniel Park, MIT License
import re
from setuptools import find_packages
from setuptools import setup


def get_version():
    filename = "gemini/__init__.py"
    with open(filename) as f:
        match = re.search(r"""^__version__ = ['"]([^'"]*)['"]""", f.read(), re.M)
    if not match:
        raise RuntimeError("{} doesn't contain __version__".format(filename))
    version = match.groups()[0]
    return version


def get_long_description():
    with open("README.md", encoding="UTF-8") as f:
        long_description = f.read()
        return long_description


version = get_version()

setup(
    name="python-gemini-api",
    version="0.1.2",
    author="daniel park",
    author_email="parkminwoo1991@gmail.com",
    description="The python package that returns Response of Google Gemini through API.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/dsdanielpark/Gemini-API",
    packages=find_packages(exclude=[]),
    python_requires=">=3.6",
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
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    entry_points={"console_scripts": ["gemini=gemini.cli:main"]},
)
