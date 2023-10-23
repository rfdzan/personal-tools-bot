from typing import Generator

from src.db.get_data import query_db


def generate_link(
    search: str, _type: str
) -> Generator[tuple[str, str, float], None, None]:
    query = query_db(search.strip(), _type)
    if _type == "movie":
        for id, title, popularity in query:
            url = rf"https://vidsrc.me/embed/movie?tmdb={id}"
            yield title, url, popularity
    if _type == "tv":
        for id, title, popularity in query:
            url = rf"https://vidsrc.me/embed/tv?tmdb={id}"
            yield title, url, popularity
