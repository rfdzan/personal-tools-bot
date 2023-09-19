import json
from typing import Generator
from os import chdir, listdir
from pathlib import Path

chdir(Path(__file__).parent.parent)


def parse_file() -> Generator[str, None, None]:
    entry = input("Filename: ")
    for file in listdir("db"):
        if entry in file:
            filename = file
    with open(f"db/{filename}", encoding="utf-8") as file:
        for line in file:
            if line is None:
                break
            text = json.loads(line)
            tmdb_id: int = text.get("id")
            if entry == "movie":
                title = "original_title"
            else:
                title = "original_name"
            tmdb_title: str = text.get(title)
            tmdb_pop: int = int(text.get("popularity"))
            yield tmdb_id, tmdb_title, tmdb_pop
