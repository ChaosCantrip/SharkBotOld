import os.path

import SharkBot as _SharkBot

_MANIFEST_FOLDER = "data/live/bungie/manifest"
_DEFINITIONS_FOLDER = f"{_MANIFEST_FOLDER}/definitions"
_MANIFEST_FILE = f"{_MANIFEST_FOLDER}/Manifest.json"
_SharkBot.Utils.FileChecker.directory(_DEFINITIONS_FOLDER)

def get_current_manifest() -> dict:
    if os.path.isfile(_MANIFEST_FILE):
        return _SharkBot.Utils.JSON.load(_MANIFEST_FILE)
    else:
        raise _SharkBot.Destiny.Errors.Manifest.ManifestNotFoundError
