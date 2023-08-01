import json
from typing import Generator
from os import chdir
from pathlib import Path
from tqdm import tqdm

chdir(Path(__file__).parent.parent)


def parse_file() -> Generator[str, None, None]:
    with open("db/movie_ids_05_15_2023.json", encoding="utf-8") as file:
        for line in file:
            if line is None:
                break
            text = json.loads(line)
            tmdb_id: int = text.get("id")
            tmdb_title: str = text.get("original_title")
            yield tmdb_id, tmdb_title