import sqlite3
from os import chdir
from pathlib import Path

chdir(Path(__file__).parent.parent)


def master_query(entry: str):
    banned_commands = ["delete", "update", "drop", "alter"]
    checklist = []
    count = 0
    loop = True
    while loop:
        for word in banned_commands:
            if word in entry:
                checklist.append(True)
                count += 1
                if count == len(checklist):
                    loop = False
            else:
                checklist.append(False)
                count += 1
                if count == len(checklist):
                    loop = False
    print(checklist)
    if any(checklist):
        return "banned command."
    else:
        conn = sqlite3.connect("db/sqlite_db/tmdb.db")
        cursor = conn.cursor()
        cursor.execute(f"{entry}")
        for data in cursor:
            yield data
