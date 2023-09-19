from typing import Generator
from os import chdir
from pathlib import Path
from db.get_data import query_db

chdir(Path(__file__).parent.parent)


def generate_link(search: str, _type: str) -> Generator[tuple[str], None, None]:
    query = query_db(search.strip(), _type)
    if _type == "movie":
        for id, title, popularity in query:
            url = rf"https://vidsrc.me/embed/movie?tmdb={id}"
            yield title, url, popularity
    if _type == "tv":
        for id, title, popularity in query:
            url = rf"https://vidsrc.me/embed/tv?tmdb={id}"
            yield title, url, popularity
