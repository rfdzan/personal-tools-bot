import sqlite3

from parse_json import parse_file
from tqdm import tqdm

from src._locations import Directories


def db_connect() -> sqlite3.Connection:
    return sqlite3.connect(Directories.TMDB_DB)


def create_table_movie(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute("PRAGMA encoding='UTF-8'")
    Q_CREATE_TABLE = (
        "CREATE TABLE IF NOT EXISTS tmdb(id INTEGER PRIMARY KEY,title TEXT)"
    )
    cursor.execute(Q_CREATE_TABLE)


def create_table_tv(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("PRAGMA encoding='UTF-8'")
    Q_CREATE_TABLE = """CREATE TABLE IF NOT EXISTS tv(
    id INTEGER PRIMARY KEY,
    title TEXT,
    popularity REAL)
    """

    cursor.execute(Q_CREATE_TABLE)


def insert_into_tv(conn: sqlite3.Connection):
    cursor = conn.cursor()
    Q_INSERT_INTO_TV = """INSERT OR IGNORE INTO tv(
    id,
    title,
    popularity
    ) VALUES(
    :id,
    :title,
    :popularity
    )
    """
    for id, title, popularity in tqdm(parse_file()):
        cursor.execute(Q_INSERT_INTO_TV, (id, title, popularity))
    conn.commit()
    conn.close()


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


def add_column_popularity_movie(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE tmdb ADD COLUMN popularity INTEGER")


def update_column_popularity_movie(conn: sqlite3.Connection):
    Q_UPDATE_POPULARITY = """UPDATE tmdb SET popularity=? WHERE id=?
    """
    with conn:
        cursor = conn.cursor()
        for id, _, popularity in tqdm(parse_file()):
            cursor.execute(Q_UPDATE_POPULARITY, (popularity, id))
        conn.commit()
    conn.close()


if __name__ == "__main__":
    # create_table_tv(db_connect())
    insert_into_tv(db_connect())
    pass
