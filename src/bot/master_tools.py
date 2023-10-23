import sqlite3
from os import chdir
from pathlib import Path
from typing import Generator

chdir(Path(__file__).parent.parent)


def master_query(entry: str) -> Generator[str, None, None] | str:
    banned_commands = ["delete", "update", "drop", "alter"]
    checklist: list[bool] = []
    count = 0
    loop = True
    while loop:
        if count == len(checklist):
            loop = False
        for word in banned_commands:  # if count clauses can be one line up top
            if word in entry:
                checklist.append(True)
                count += 1
            else:
                checklist.append(False)
                count += 1

    if any(checklist):
        return "banned command."
    else:
        conn = sqlite3.connect("db/sqlite_db/tmdb.db")
        cursor = conn.cursor()
        cursor.execute(f"{entry}")
        for data in cursor:
            yield data
    return None
