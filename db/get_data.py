import sqlite3
from typing import Generator
from os import chdir
from pathlib import Path

chdir(Path(__file__).parent.parent)


def db_connect() -> sqlite3.Connection:
    return sqlite3.connect("db/sqlite_db/tmdb.db")


def query_db(search: str) -> Generator[str, None, None]:
    search = search.replace(" ", "%")
    conn = db_connect()
    with conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM tmdb WHERE title LIKE ? ORDER BY popularity DESC ",
            (f"%{search}%",),
        )
        for id, title, popularity in cursor:
            yield id, title, popularity
