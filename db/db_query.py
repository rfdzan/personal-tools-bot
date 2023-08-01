import sqlite3
from parse_json import parse_file
from os import chdir
from pathlib import Path
from tqdm import tqdm

chdir(Path(__file__).parent.parent)


def db_connect():
    return sqlite3.connect("db/sqlite_db/tmdb3.db")


def create_table(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("PRAGMA encoding='UTF-8'")
    # Q_CREATE_TABLE = "CREATE TABLE IF NOT EXISTS tmdb(id INTEGER PRIMARY KEY,title TEXT)STRICT"
    Q_CREATE_TABLE = (
        "CREATE TABLE IF NOT EXISTS tmdb(id INTEGER PRIMARY KEY,title TEXT) STRICT"
    )
    cursor.execute(Q_CREATE_TABLE)


def insert_into_tmdb(conn: sqlite3.Connection):
    Q_INSERT_INTO_TMDD = """INSERT OR IGNORE INTO tmdb(
    id,
    title
    ) VALUES(
    :id,
    :title
    )
    """

    cursor = conn.cursor()
    for id, title in tqdm(parse_file()):
        cursor.execute(Q_INSERT_INTO_TMDD, (id, title))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table(db_connect())
    insert_into_tmdb(db_connect())
