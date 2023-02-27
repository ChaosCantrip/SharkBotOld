import os.path
import logging
from typing import Optional

import requests
import aiohttp
import colorama

import SharkBot as _SharkBot
import SharkBot.Errors

manifest_logger = logging.getLogger("manifest")
setup_logger = logging.getLogger("manifest_setup")

_MANIFEST_FOLDER = "data/live/bungie/manifest"
_DEFINITIONS_FOLDER = f"{_MANIFEST_FOLDER}/definitions"
_MANIFEST_FILE = f"{_MANIFEST_FOLDER}/Manifest.json"
_SharkBot.Utils.FileChecker.directory(_DEFINITIONS_FOLDER)

def get_current_manifest() -> dict:
    if os.path.isfile(_MANIFEST_FILE):
        return _SharkBot.Utils.JSON.load(_MANIFEST_FILE)
    else:
        raise _SharkBot.Errors.Manifest.ManifestNotFoundError

def initial_setup():
    print(SharkBot.Utils.Colours.cyan("\n----- Manifest Initial Setup -----"))
    setup_logger.info("Checking for Existing Manifest")
    print(SharkBot.Utils.Colours.yellow("Checking for Existing Manifest"))
    manifest_outdated = False
    manifest_data = None
    if not os.path.isfile(_MANIFEST_FILE):
        setup_logger.warning("No Manifest Found")
        print(SharkBot.Utils.Colours.red("No Manifest Found"))
        _response = requests.get("https://www.bungie.net/Platform/Destiny2/Manifest/")
        if not _response.ok:
            setup_logger.error(f"Failed to fetch Manifest - [{_response.status_code}]")
            print(SharkBot.Utils.Colours.red(f"Failed to fetch Manifest - [{_response.status_code}]"))
            return
        manifest_data = _response.json()
        manifest_outdated = True
    else:
        manifest_version = SharkBot.Utils.JSON.load(_MANIFEST_FILE)["Response"]["version"]
        setup_logger.info(f"Manifest Found - '{manifest_version}' - Checking for Update")
        print(SharkBot.Utils.Colours.green(f"Manifest Found - '{manifest_version}' - Checking for Update"))
        _response = requests.get("https://www.bungie.net/Platform/Destiny2/Manifest/")
        if not _response.ok:
            setup_logger.error(f"Failed to fetch Manifest Update - [{_response.status_code}]")
            print(SharkBot.Utils.Colours.red(f"Failed to fetch Manifest Update - [{_response.status_code}]"))
            return
        manifest_data = _response.json()
        new_version = manifest_data["Response"]["version"]
        manifest_outdated = new_version != manifest_version

    if manifest_outdated:
        setup_logger.warning(f"Manifest Outdated, Downloading")
        print(SharkBot.Utils.Colours.green(f"Manifest Outdated, Downloading"))
        _version = manifest_data["Response"]["version"]
        SharkBot.Utils.JSON.dump(_MANIFEST_FILE, manifest_data)
        setup_logger.info(f"Saved Manifest - '{_version}'")
        print(SharkBot.Utils.Colours.yellow(f"Saved Manifest - '{_version}'"))
        print(SharkBot.Utils.Colours.cyan(f"Downloading Definitions ["), end="")
        for definition_name, definition_url in manifest_data["Response"]["jsonWorldComponentContentPaths"]["en"].items():
            _response = requests.get(f"https://www.bungie.net/{definition_url}")
            if not _response.ok:
                setup_logger.error(f"Failed to fetch {definition_name} - [{_response.status_code}]")
                print(SharkBot.Utils.Colours.red("-"), end="")
                continue
            SharkBot.Utils.JSON.dump(f"{_DEFINITIONS_FOLDER}/{definition_name}.json", _response.json())
            setup_logger.info(f"Downloaded {definition_name}")
            print(SharkBot.Utils.Colours.green("-"), end="")
        print(SharkBot.Utils.Colours.cyan("]"))
        setup_logger.info("Manifest Downloaded")
        print(SharkBot.Utils.Colours.green("Manifest Downloaded"))
    else:
        setup_logger.info(f"Manifest Up to Date")
        print(SharkBot.Utils.Colours.green(f"Manifest Up to Date"))
    print(SharkBot.Utils.Colours.cyan("----- Manifest Setup Finished-----\n"))

initial_setup()

POSSIBLE_DEFINITIONS: list[str] = []
DEFINITIONS_LOOKUP: dict[str, dict] = {}
MANIFEST_VERSION: Optional[str] = None
try:
    current = get_current_manifest()["Response"]
    POSSIBLE_DEFINITIONS = current["jsonWorldComponentContentPaths"]["en"].keys()
    DEFINITIONS_LOOKUP = {_definition.lower(): None for _definition in POSSIBLE_DEFINITIONS}
    MANIFEST_VERSION = current["version"]
    print(colorama.Fore.GREEN + "Loaded Manifest Possible Definitions")
    setup_logger.info("Loaded Manifest Possible Definitions")
except _SharkBot.Errors.Manifest.ManifestNotFoundError:
    print(colorama.Fore.RED + "Manifest Possible Definitions Load Aborted - ManifestNotFound")
    setup_logger.info("Manifest Possible Definitions Load Aborted - ManifestNotFound")
    pass

def get_definitions_file(definition_type: str):
    if definition_type.lower() not in DEFINITIONS_LOOKUP.keys():
        raise SharkBot.Errors.Manifest.DefinitionDoesNotExistError(definition_type)
    if DEFINITIONS_LOOKUP[definition_type.lower()] is None:
        manifest_logger.info(f"Loading {definition_type} into Memory")
        try:
            DEFINITIONS_LOOKUP[definition_type.lower()] = SharkBot.Utils.JSON.load(f"{_DEFINITIONS_FOLDER}/{definition_type}.json")
        except FileNotFoundError:
            manifest_logger.error(f"Failed to load {definition_type} into Memory - File Not Found")
            raise SharkBot.Errors.Manifest.DefinitionFileNotFoundError(definition_type)
    return DEFINITIONS_LOOKUP[definition_type.lower()]


def get_definition(definition_type: str, item_hash: str | int) -> dict:
    _definitions_file = get_definitions_file(definition_type)
    try:
        return _definitions_file[str(item_hash)]
    except KeyError:
        raise _SharkBot.Errors.Manifest.HashNotFoundError(definition_type, item_hash)

def get_definitions_by_name(definition_type: str, item_name: str) -> list[dict]:
    _definitions_file = get_definitions_file(definition_type)
    item_name = item_name.lower()
    return [
        _definition for _definition in _definitions_file.values() if _definition.get("displayProperties", {}).get("name", "").lower() == item_name
    ]

async def fetch_manifest(write: bool = True):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.bungie.net/Platform/Destiny2/Manifest/") as response:
            if response.ok:
                _data = await response.json()
                if write:
                    global POSSIBLE_DEFINITIONS
                    global DEFINITIONS_LOOKUP
                    POSSIBLE_DEFINITIONS = _data["Response"]["jsonWorldComponentContentPaths"]["en"].keys()
                    DEFINITIONS_LOOKUP = {_definition[7:-10].lower(): _definition for _definition in POSSIBLE_DEFINITIONS}
                    _SharkBot.Utils.JSON.dump(_MANIFEST_FILE, _data)
                return _data
            else:
                raise _SharkBot.Errors.Manifest.FetchFailedError("Manifest", response.status)

async def is_outdated() -> bool:
    not_found = False
    _old_manifest = None
    try:
        _old_manifest = get_current_manifest()
    except _SharkBot.Errors.Manifest.ManifestNotFoundError:
        not_found = True
    _new_manifest = await fetch_manifest(write=False)
    return not_found or _old_manifest["Response"]["version"] != _new_manifest["Response"]["version"]