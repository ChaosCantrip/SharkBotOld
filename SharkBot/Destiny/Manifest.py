import os.path
import logging

import aiohttp
import colorama

import SharkBot as _SharkBot
import SharkBot.Errors

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

def get_definitions_file(definition_type: str):
    try:
        _filepath = f"{_DEFINITIONS_FOLDER}/{_DEFINITIONS_LOOKUP[definition_type.lower()]}.json"
    except KeyError:
        raise SharkBot.Errors.Manifest.DefinitionDoesNotExistError(definition_type)
    if os.path.isfile(_filepath):
        return _SharkBot.Utils.JSON.load(_filepath)
    else:
        raise _SharkBot.Errors.Manifest.DefinitionFileNotFoundError(definition_type)

def get_definition(definition_type: str, item_hash: str | int) -> dict:
    _definitions_file = get_definitions_file(definition_type)
    try:
        return _definitions_file[str(item_hash)]
    except KeyError:
        raise _SharkBot.Errors.Manifest.HashNotFoundError(definition_type, item_hash)

async def fetch_manifest(write: bool = True):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.bungie.net/Platform/Destiny2/Manifest/") as response:
            if response.ok:
                _data = await response.json()
                if write:
                    _SharkBot.Utils.JSON.dump(_MANIFEST_FILE, _data)
                return _data
            else:
                raise _SharkBot.Errors.Manifest.FetchFailedError("Manifest", response.status)

async def fetch_definition_file(definition_type: str, write: bool = True):
    try:
        _definition_location = get_current_manifest()["Response"]["jsonWorldComponentContentPaths"]["en"][definition_type]
    except KeyError:
        raise _SharkBot.Errors.Manifest.DefinitionDoesNotExistError(definition_type)
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://www.bungie.net/{_definition_location}") as response:
            if response.ok:
                _data = await response.json()
                if write:
                    _SharkBot.Utils.JSON.dump(f"{_DEFINITIONS_FOLDER}/{definition_type}.json", _data)
                return _data
            else:
                raise _SharkBot.Errors.Manifest.FetchFailedError(definition_type, response.status)


