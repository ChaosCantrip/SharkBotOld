import os.path
import logging
import colorama

import SharkBot as _SharkBot

manifest_logger = logging.getLogger("manifest")

_MANIFEST_FOLDER = "data/live/bungie/manifest"
_DEFINITIONS_FOLDER = f"{_MANIFEST_FOLDER}/definitions"
_MANIFEST_FILE = f"{_MANIFEST_FOLDER}/Manifest.json"
_SharkBot.Utils.FileChecker.directory(_DEFINITIONS_FOLDER)

def get_current_manifest() -> dict:
    if os.path.isfile(_MANIFEST_FILE):
        return _SharkBot.Utils.JSON.load(_MANIFEST_FILE)
    else:
        raise _SharkBot.Errors.Manifest.ManifestNotFoundError

_POSSIBLE_DEFINITIONS: list[str] = []
_DEFINITIONS_LOOKUP: dict[str, str] = {}
try:
    _POSSIBLE_DEFINITIONS = get_current_manifest()["Response"]["jsonWorldComponentContentPaths"]["en"].keys()
    _DEFINITIONS_LOOKUP = {_definition[7:-10].lower(): _definition for _definition in _POSSIBLE_DEFINITIONS}
    print(colorama.Fore.GREEN + "Loaded Manifest Possible Definitions")
    manifest_logger.info("Loaded Manifest Possible Definitions")
except _SharkBot.Errors.Manifest.ManifestNotFoundError:
    print(colorama.Fore.RED + "Manifest Possible Definitions Load Aborted - ManifestNotFound")
    manifest_logger.info("Manifest Possible Definitions Load Aborted - ManifestNotFound")
    pass