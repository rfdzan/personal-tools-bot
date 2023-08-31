from dataclasses import dataclass
from pathlib import PurePath


@dataclass
class Directories:
    APP_DIR = PurePath(__file__).parents[0]
    MAIN_DIR = PurePath(__file__).parents[1]
    SAMPLE_TEXT = MAIN_DIR.joinpath("sample_text")
