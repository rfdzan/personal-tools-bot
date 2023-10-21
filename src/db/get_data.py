import sqlite3
from typing import Generator

from src._locations import Directories


def db_connect() -> sqlite3.Connection:
    return sqlite3.connect(Directories.TMDB_DB)


def query_db(search: str, _type: str) -> Generator[str, None, None]:
    search = search.replace(" ", "%")
    conn = db_connect()
    with conn:
        cursor = conn.cursor()
        if _type == "movie":
            cursor.execute(
                "SELECT * FROM tmdb WHERE title LIKE ? ORDER BY popularity DESC ",
                (f"%{search}%",),
            )
            for id, title, popularity in cursor:
                yield id, title, popularity
        if _type == "tv":
            cursor.execute(
                "SELECT * FROM tv WHERE title LIKE ? ORDER BY popularity DESC ",
                (f"%{search}%",),
            )
            for id, title, popularity in cursor:
                yield id, title, popularity
