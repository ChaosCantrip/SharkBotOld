import sqlite3
import json

from SharkBot import Errors

_MANIFEST_FOLDER = "data/live/bungie/manifest"
_CONTENT_FILE = _MANIFEST_FOLDER + "/manifest.content"

con = sqlite3.connect(_CONTENT_FILE)

def _execute(statement: str, fetch_all: bool = True):
    cur = con.cursor()
    if fetch_all:
        res = cur.execute(statement).fetchall()
    else:
        res = cur.execute(statement).fetchone()
    cur.close()
    return res

DEFINITION_TYPES = [r[0] for r in _execute("SELECT name FROM sqlite_master WHERE type='table';")]

_HASH_THRESHOLD = 2**31 - 1
_HASH_MODIFIER = 2**32

def _hash_to_id(hash_in: str | int) -> int:
    hash_in = int(hash_in)
    if hash_in > _HASH_THRESHOLD:
        return hash_in - _HASH_MODIFIER
    else:
        return hash_in

def get_definition(definition_type: str, definition_hash: str | int):
    if definition_type not in DEFINITION_TYPES:
        raise Errors.Manifest.DefinitionTypeDoesNotExistError(definition_type)
    definition_id = _hash_to_id(definition_hash)
    result = _execute(f"SELECT * FROM {definition_type} WHERE id={definition_id}", fetch_all=False)
    if result is None:
        raise Errors.Manifest.HashNotFoundError(definition_type, definition_hash, definition_id)
    else:
        return json.loads(result[1])