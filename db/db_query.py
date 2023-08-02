import sqlite3
from parse_json import parse_file
from os import chdir
from pathlib import Path
from tqdm import tqdm

chdir(Path(__file__).parent.parent)


def db_connect() -> sqlite3.Connection:
    return sqlite3.connect("db/sqlite_db/tmdb.db")


def create_table(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute("PRAGMA encoding='UTF-8'")
    # Q_CREATE_TABLE = "CREATE TABLE IF NOT EXISTS tmdb(id INTEGER PRIMARY KEY,title TEXT)STRICT"
    Q_CREATE_TABLE = (
        "CREATE TABLE IF NOT EXISTS tmdb(id INTEGER PRIMARY KEY,title TEXT)"
    )
    cursor.execute(Q_CREATE_TABLE)


def insert_into_tmdb(conn: sqlite3.Connection) -> None:
    Q_INSERT_INTO_TMDD = """INSERT OR IGNORE INTO tmdb(
    id,
    title,
    popularity
    ) VALUES(
    :id,
    :title,
    :popularity
    )
    """

    cursor = conn.cursor()
    for id, title, popularity in tqdm(parse_file()):
        cursor.execute(Q_INSERT_INTO_TMDD, (id, title, popularity))
    conn.commit()
    conn.close()


def add_column_popularity(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE tmdb ADD COLUMN popularity INTEGER")


def update_column_popularity(conn: sqlite3.Connection):
    Q_UPDATE_POPULARITY = """UPDATE tmdb SET popularity=? WHERE id=?
    """
    with conn:
        cursor = conn.cursor()
        for id, _, popularity in tqdm(parse_file()):
            cursor.execute(Q_UPDATE_POPULARITY, (popularity, id))
        conn.commit()
    conn.close()


if __name__ == "__main__":
    # create_table(db_connect())
    # insert_into_tmdb(db_connect())
    add_column_popularity(db_connect())
    update_column_popularity(db_connect())
1
