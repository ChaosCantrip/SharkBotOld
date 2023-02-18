import json
import os.path
from datetime import datetime, timedelta
from typing import Optional, Union, TypedDict, Self
import aiohttp
import secret
import logging

from .BungieData import Craftables, Monument

bungie_logger = logging.getLogger("bungie")

import SharkBot

_RACES = {
    0: "Human",
    1: "Awoken",
    2: "Exo"
}

_CLASSES = {
    0: "Titan",
    1: "Hunter",
    2: "Warlock"
}

class _Guardian:

    def __init__(self, character_data: dict):
        self._race = _RACES[character_data["raceType"]]
        self._class = _CLASSES[character_data["classType"]]

    @property
    def icon(self) -> str:
        return SharkBot.Icon.get(f"class_{self._class}")

    def __str__(self) -> str:
        return f"{self.icon} {self._race} {self._class}"

class _CacheFolders:
    CORE = "data/live/bungie/cache"
    CRAFTABLES = CORE + "/craftables"
    WEAPON_LEVELS = CORE + "/weapon_levels"
    CURRENCY = CORE + "/currencies"
    LIST = [CRAFTABLES, WEAPON_LEVELS, CURRENCY]

SharkBot.Utils.FileChecker.directory(_CacheFolders.CRAFTABLES)
SharkBot.Utils.FileChecker.directory(_CacheFolders.WEAPON_LEVELS)
SharkBot.Utils.FileChecker.directory(_CacheFolders.CURRENCY)

with open("data/static/bungie/definitions/CraftableWeaponHashes.json", "r") as infile:
    _CRAFTABLE_WEAPON_HASHES: dict[str, str] = json.load(infile)

with open("data/static/bungie/definitions/CraftingWeaponTypes.json", "r") as infile:
    _CRAFTABLE_WEAPON_TYPES: dict[str, str] = json.load(infile)

with open("data/static/bungie/definitions/LevelObjectiveHashes.json", "r") as infile:
    _data = json.load(infile)
    _WEAPON_LEVEL_RECORDS: list[str] = _data["records"]
    _LEVEL_OBJECTIVE_HASH: int = _data["objective"]

with open("data/static/bungie/definitions/CurrencyHashes.json", "r") as infile:
    _CURRENCY_HASHES: dict[str, str] = json.load(infile)

with open("data/static/bungie/definitions/BountiesSorted.json", "r") as infile:
    _BOUNTY_REFERENCE: dict[str, list[str]] = json.load(infile)

_CURRENCY_ORDER = [
    "Glimmer",
    "Bright Dust",
    "Legendary Shards",
    "Enhancement Core",
    "Enhancement Prism",
    "Ascendant Shard",
    "Upgrade Module",
    "Ascendant Alloy",
    "Resonant Alloy",
    "Strange Coin"
]


class MemberBungie:

    def __init__(self, member, token: Optional[str] = None, token_expires: Optional[int] = None,
                 refresh_token_expires: Optional[int] = None, destiny_membership_id: Optional[str] = None,
                 destiny_membership_type: Optional[int] = None):
        self._member: SharkBot.Member.Member = member
        self._token = token
        self._token_expires = token_expires
        self._refresh_token_expires = refresh_token_expires
        self._destiny_membership_id = destiny_membership_id
        self._destiny_membership_type = destiny_membership_type
        self.craftables = Craftables(self._member)
        self.monument = Monument(self._member)

    def delete_credentials(self) -> bool:
        self._token = None
        self._token_expires = None
        self._refresh_token_expires = None
        self._destiny_membership_id = None
        self._destiny_membership_type = None

        db = SharkBot.Handlers.firestoreHandler.db
        doc_ref = db.collection(u"bungieauth").document(str(self._member.id))
        doc = doc_ref.get()

        if not doc.exists:
            return False
        else:
            doc_ref.delete()
            return True

    @property
    def refresh_token_expiring(self) -> bool:
        if self._refresh_token_expires is None:
            return False
        else:
            return self._refresh_token_expires < (datetime.utcnow() + timedelta(weeks=1)).timestamp()

    async def soft_refresh(self):
        try:
            await self._refresh_token()
        except Exception as e:
            pass

    async def _refresh_token(self) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.get(secret.BungieAPI.REFRESH_URL, data=secret.BungieAPI.refresh_headers(self._member.id)) as response:
                if response.ok:
                    bungie_logger.info(f"{self._member.id} {self._member.raw_display_name} - Token Refresh Successful")
                    return True
                else:
                    bungie_logger.error(f"{self._member.id} {self._member.raw_display_name} - Token Refresh Unsuccessful")
                    return False

    def _need_refresh(self) -> bool:
        if self._token_expires is None:
            return True
        else:
            return self._token_expires < datetime.utcnow().timestamp() - 60

    async def _get_token(self):
        if self._token is not None:
            if not self._need_refresh():
                return self._token

        doc_ref = SharkBot.Handlers.firestoreHandler.db.collection(u"bungieauth").document(str(self._member.id))
        doc = doc_ref.get()

        if not doc.exists:
            raise SharkBot.Errors.BungieAPI.SetupNeededError(self._member.id)

        if not await self._refresh_token():
            raise SharkBot.Errors.BungieAPI.InternalServerError(self._member.id)

        doc = doc_ref.get()

        data = doc.to_dict()
        self._token = data["access_token"]
        self._token_expires = datetime.utcnow().timestamp() + data["expires_in"]
        self._refresh_token_expires = data["refresh_expires_in"] + data["refreshed_at"]
        self._destiny_membership_id = data["destiny_membership_id"]
        self._destiny_membership_type = data["destiny_membership_type"]
        bungie_logger.info(f"{self._member.id} {self._member.raw_display_name} - Retrieved Token")
        self._member.write_data()
        return self._token

    def wipe_all_cache(self):
        for cache_folder in _CacheFolders.LIST:
            if os.path.isfile(f"{cache_folder}/{self._member.id}.json"):
                os.remove(f"{cache_folder}/{self._member.id}.json")


    async def get_endpoint_data(self, *components: int) -> dict[str, dict]:
        _components_string = ",".join(str(component) for component in components)
        token = await self._get_token()
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://www.bungie.net/Platform/Destiny2/{self._destiny_membership_type}/Profile/{self._destiny_membership_id}?components={_components_string}",
                    headers=secret.BungieAPI.bungie_headers(token)
            ) as response:
                if not response.ok:
                    bungie_logger.error(f"{self._member.id} {self._member.raw_display_name} - Endpoint Unsuccessful - Response {response.status} [{_components_string}]")
                    self._token = None
                    raise SharkBot.Errors.BungieAPI.InternalServerError
                else:
                    bungie_logger.info(f"{self._member.id} {self._member.raw_display_name} - Endpoint Successful - Response {response.status} [{_components_string}]")
                    data = await response.json()
                    return data

    async def get_profile_response(self, *components: int) -> dict[str, dict]:
        data = await self.get_endpoint_data(*components)
        return data["Response"]

    async def get_currency_data(self) -> dict[str, int]:
        data = await self.get_profile_response(600)
        currency_data = data["characterCurrencyLookups"]["data"]
        result_data = {item_name: 0 for item_name in _CURRENCY_ORDER}
        for character_data in currency_data.values():
            quantities = character_data["itemQuantities"]
            for item_hash, quantity in quantities.items():
                item_name = _CURRENCY_HASHES.get(item_hash)
                if item_name is None:
                    continue
                else:
                    result_data[item_name] += quantity

        result = {}
        for item_name, quantity in result_data.items():
            icon_name = SharkBot.Icon.get("currency_" + "_".join(item_name.lower().split(" ")))
            result[f"{icon_name} {item_name}"] = int(quantity/3)
        self.write_currency_cache(result)
        return result

    def get_cached_currency_data(self) -> Optional[dict[str, int]]:
        if not os.path.isfile(_CacheFolders.CURRENCY + f"/{self._member.id}.json"):
            return None
        else:
            with open(_CacheFolders.CURRENCY + f"/{self._member.id}.json", "r") as _infile:
                data = json.load(_infile)
            return data

    def write_currency_cache(self, raw_data: dict[str, int]):
        with open(_CacheFolders.CURRENCY + f"/{self._member.id}.json", "w+") as _outfile:
            json.dump(raw_data, _outfile, indent=2)

    def get_cached_weapon_levels_data(self) -> Optional[list[list[str, int, str]]]:
        if not os.path.isfile(_CacheFolders.WEAPON_LEVELS + f"/{self._member.id}.json"):
            return None
        else:
            with open(_CacheFolders.WEAPON_LEVELS + f"/{self._member.id}.json", "r") as _infile:
                data = json.load(_infile)
            return data

    def write_weapon_levels_cache(self, raw_data: list[list[str, int, str]]):
        with open(_CacheFolders.WEAPON_LEVELS + f"/{self._member.id}.json", "w+") as _outfile:
            json.dump(raw_data, _outfile, indent=2)

    async def get_weapon_levels_data(self) -> list[list[str, int, str]]:
        data = await self.get_profile_response(102,201,205,309)
        item_components: dict[str, dict] = data["itemComponents"]["plugObjectives"]["data"]
        items: list[dict] = list(item for item in data["profileInventory"]["data"]["items"] if "itemInstanceId" in item)
        for bucket in ["characterInventories", "characterEquipment"]:
            bucket_data: dict[str, dict[str, list[dict]]] = data[bucket]["data"]
            for item_set in bucket_data.values():
                items.extend(item for item in item_set["items"] if "itemInstanceId" in item)

        weapons_with_levels: list[list[str, int, str]] = []

        for item in items:
            item_instance = item_components.get(item["itemInstanceId"])
            if item_instance is None:
                continue
            item_objectives: dict[str, list] = item_instance["objectivesPerPlug"]
            shaped_record = None
            for record_hash in _WEAPON_LEVEL_RECORDS:
                shaped_record = item_objectives.get(record_hash)
                if shaped_record is not None:
                    break
            if shaped_record is not None:
                item_name = _CRAFTABLE_WEAPON_HASHES[str(item["itemHash"])]
                level_record = [record for record in shaped_record if record["objectiveHash"] == _LEVEL_OBJECTIVE_HASH][0]
                item_type = _CRAFTABLE_WEAPON_TYPES[item_name]
                weapons_with_levels.append([item_name, level_record["progress"], item_type])

        self.write_weapon_levels_cache(weapons_with_levels)

        return weapons_with_levels

    async def get_bounty_prep_data(self) -> dict[str, dict[str, Union[int, dict[str, int]]]]:
        data = await self.get_profile_response(200,201,301)
        character_data: dict[str, dict] = data["characters"]["data"]
        character_inventories_data: dict[str, dict[str, list[dict]]] = data["characterInventories"]["data"]
        objective_data: dict[str, dict[str, list[dict]]] = data["itemComponents"]["objectives"]["data"]
        result = {}
        for character_hash, inventory_data in character_inventories_data.items():
            guardian = _Guardian(character_data[character_hash])
            processed_data = {
                "Total": 0,
                "Weekly": {
                    "Clan": 0,
                    "Dreaming City": 0,
                    "Europa": 0,
                    "Moon": 0,
                    "Eternity": 0
                },
                "Vanguard": 0,
                "Crucible": 0,
                "Gambit": 0,
                "Daily": 0,
                "Gunsmith": 0,
                "Repeatable": 0,
                "Useless": [],
                "Incomplete": []
            }
            for item_data in inventory_data["items"]:
                bounty_data = _BOUNTY_REFERENCE.get(str(item_data["itemHash"]))
                if bounty_data is None:
                    continue
                bounty_instance = objective_data[item_data["itemInstanceId"]]
                processed_data["Total"] += 1
                bounty_type, bounty_source, bounty_name = bounty_data
                bounty_complete = all([objective["complete"] for objective in bounty_instance["objectives"]])
                if not bounty_complete:
                    if bounty_type not in ["Repeatable", "Useless"]:
                        processed_data["Incomplete"].append([bounty_name, bounty_source])
                        continue
                if bounty_type == "Weekly":
                    processed_data["Weekly"][bounty_source] = processed_data["Weekly"].get(bounty_source, 0) + 1
                elif bounty_type == "Useless":
                    processed_data["Useless"].append([bounty_name, bounty_source])
                else:
                    processed_data[bounty_type] += 1
            result[f"{guardian} `({processed_data['Total']}/63)`"] = processed_data
        return result


    @property
    def data(self) -> dict:
        return {
            "token": self._token,
            "token_expires": self._token_expires,
            "refresh_token_expires": self._refresh_token_expires,
            "destiny_membership_id": self._destiny_membership_id,
            "destiny_membership_type": self._destiny_membership_type
        }
