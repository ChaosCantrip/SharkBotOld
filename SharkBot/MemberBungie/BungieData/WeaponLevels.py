from .BungieData import BungieData
import SharkBot

_CRAFTABLE_WEAPON_HASHES: dict[str, str] = SharkBot.Utils.JSON.load("data/static/bungie/definitions/CraftableWeaponHashes.json")

_CRAFTABLE_WEAPON_TYPES: dict[str, str] = SharkBot.Utils.JSON.load("data/static/bungie/definitions/CraftingWeaponTypes.json")

_data = SharkBot.Utils.JSON.load("data/static/bungie/definitions/LevelObjectiveHashes.json")
_WEAPON_LEVEL_RECORDS: list[str] = _data["records"]
_LEVEL_OBJECTIVE_HASH: int = _data["objective"]

class WeaponLevels(BungieData):
    _COMPONENTS = [102,201,205,309]

    @staticmethod
    def _process_data(data):
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

        return weapons_with_levels