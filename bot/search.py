from os import chdir
from pathlib import Path
from db.get_data import query_db

chdir(Path(__file__).parent.parent)


def generate_link(search: str):
    query = query_db(search=search.strip())
    for id, title in query:
        url = rf"https://vidsrc.me/embed/movie?tmdb={id}"
        yield title, url
