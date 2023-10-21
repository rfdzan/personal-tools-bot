from dataclasses import dataclass
from pathlib import PurePath


@dataclass
class Directories:
    PROJ_DIR = PurePath(__file__).parents[0]
    BOT_DIR = PROJ_DIR.joinpath("bot")
    DB_DIR = PROJ_DIR.joinpath("db")
    TOKPED_SEARCH = PROJ_DIR.joinpath("search")
    TMDB_DB = DB_DIR.joinpath("sqlite_db", "tmdb.db")
