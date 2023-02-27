import sqlite3

_MANIFEST_FOLDER = "data/live/bungie/manifest"
_CONTENT_FILE = _MANIFEST_FOLDER + "/manifest.content"

con = sqlite3.connect(_CONTENT_FILE)

def _execute(statement: str):
    cur = con.cursor()
    res = cur.execute(statement).fetchall()
    cur.close()
    return res

DEFINITION_TYPES = [r[0] for r in _execute("SELECT name FROM sqlite_master WHERE type='table';")]