from enum import Enum


class FreeModel(Enum):
    GEMMA_7B = "google/gemma-7b-it:free"
    ZEPHYR_7B = "huggingfaceh4/zephyr-7b-beta:free"
    MISTRAL_7B = "mistralai/mistral-7b-instruct:free"
    CINEMATIKA_7B = "openrouter/cinematika-7b:free"
    TOPPY_M_7B = "undi95/toppy-m-7b:free"
    MYTHOMIST_7B = "gryphe/mythomist-7b:free"
    CAPYBARA_7B = "nousresearch/nous-capybara-7b:free"
    OPENCHAT_7B = "openchat/openchat-7b:free"


FREE_MODELS = {member.value for member in FreeModel}
