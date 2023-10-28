from pathlib import PurePath

PROJ_DIR = PurePath(__file__).parents[1]
SRC = PROJ_DIR.joinpath("steam_search")
FILES = SRC.joinpath("files")
