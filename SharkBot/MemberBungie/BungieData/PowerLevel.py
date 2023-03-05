import discord

from .BungieData import BungieData
import SharkBot

_FRACTIONS = {
    1/8: "⅛",
    2/8: "²⁄₈",
    3/8: "⅜",
    4/8: "⁴⁄₈",
    5/8: "⅝",
    6/8: "⁶⁄₈",
    7/8: "⅞"
}

class HashTranslations:
    STAT_HASHES = {
        3897883278: "Armour",
        1480404414: "Weapons",
        3289069874: "Power Bonus"
    }
    WEAPON_TYPES = {
        2: "Kinetic",
        3: "Energy",
        4: "Power"
    }
    ARMOUR_CLASSES = {
        21: "Warlock",
        22: "Titan",
        23: "Hunter"
    }
    ARMOUR_SLOTS = {
        45: "Head",
        46: "Arms",
        47: "Chest",
        48: "Legs",
        49: "Class"
    }

def _create_blank_dataset():
    return {
        "Weapons": {
            "Kinetic": 0,
            "Energy": 0,
            "Power": 0
        },
        "Titan": {
            "Head": 0,
            "Arms": 0,
            "Chest": 0,
            "Legs": 0,
            "Class": 0
        },
        "Warlock": {
            "Head": 0,
            "Arms": 0,
            "Chest": 0,
            "Legs": 0,
            "Class": 0
        },
        "Hunter": {
            "Head": 0,
            "Arms": 0,
            "Chest": 0,
            "Legs": 0,
            "Class": 0
        },
        "Power Bonus": 0
    }

class PowerLevel(BungieData):
    _COMPONENTS = [102,201,205,300]
    _THUMBNAIL_URL = None

    @staticmethod
    def _process_data(data):
        # Get All Item Buckets
        item_buckets: list[list[dict]] = [data["profileInventory"]["data"]["items"]]
        for bucket_location in ["characterInventories", "characterEquipment"]:
            for bucket_data in data[bucket_location]["data"].values():
                item_buckets.append(bucket_data["items"])

        raw_data = _create_blank_dataset()
        item_instances: dict[str, dict] = data["itemComponents"]["instances"]["data"]
        results: dict[str, dict[str, int | dict[str, int]]] = {}
        for bucket in item_buckets:
            for item in bucket:
                if (item_instance_id:=item.get("itemInstanceId")) is None:
                    continue
                item_instance = item_instances[str(item_instance_id)]
                if (primary_stat:=item_instance.get("primaryStat")) is None:
                    continue
                if (item_type:=HashTranslations.STAT_HASHES.get(primary_stat["statHash"])) is None:
                    continue
                stat_value: int = primary_stat["value"]
                if item_type == "Power Bonus":
                    raw_data["Power Bonus"] = max(stat_value, raw_data["Power Bonus"])
                    continue
                item_category_hashes: list[str] = SharkBot.Destiny.Definitions.DestinyInventoryItemDefinition.get(item["itemHash"])["itemCategoryHashes"]
                item_sub_type = None
                if item_type == "Armour":
                    for category_hash, category_name in HashTranslations.ARMOUR_CLASSES.items():
                        if category_hash in item_category_hashes:
                            item_type = category_name
                            break
                    for category_hash, category_name in HashTranslations.ARMOUR_SLOTS.items():
                        if category_hash in item_category_hashes:
                            item_sub_type = category_name
                            break
                else: # Weapons
                    for category_hash, category_name in HashTranslations.WEAPON_TYPES.items():
                        if category_hash in item_category_hashes:
                            item_sub_type = category_name
                            break
                if stat_value > raw_data[item_type][item_sub_type]:
                    raw_data[item_type][item_sub_type] = stat_value
            power_bonus = raw_data["Power Bonus"]
            for class_name in HashTranslations.ARMOUR_CLASSES.values():
                raw_items = dict(raw_data["Weapons"])
                raw_items |= raw_data[class_name]
                items = {
                    item_type: {
                        "Power": item_power,
                        "Difference": None
                    } for item_type, item_power in raw_items.items()
                }
                raw_power_level = sum([item["Power"] for item in items.values()]) / 8
                power_level = int(raw_power_level)
                raw_power_level -= power_level
                raw_power_level = f"{power_level} {_FRACTIONS[raw_power_level]}"
                for item_data in items.values():
                    item_data["Difference"] = str(item_data["Power"] - power_level)
                    if not item_data["Difference"].startswith("-"):
                        item_data["Difference"] = "+" + item_data["Difference"]
                results[class_name] = {
                    "Equipment Power Level": raw_power_level,
                    "Power Level": power_level,
                    "Power Bonus": power_bonus,
                    "Items": items
                }
        return results

    # @staticmethod
    # def _process_cache_write(data):
    #     return data

    # @staticmethod
    # def _process_cache_load(data):
    #     return data

    # @classmethod
    # def _format_cache_embed_data(cls, embed: discord.Embed, data, **kwargs):
    #     cls._format_embed_data(embed, data)

    @staticmethod
    def _format_embed_data(embed: discord.Embed, data, **kwargs):
        for class_name, class_data in data.items():
            class_header = f"__*{class_data['Equipment Power Level']} + {class_data['Power Bonus']}*__"
            embed.add_field(
                name=f"{class_name}: {class_data['Power Level'] + class_data['Power Bonus']}",
                value=class_header + "\n" + "\n".join(
                    f"{item_type}: `{item_data['Power']} ({item_data['Difference']})`" for item_type, item_data in class_data["Items"].items()
                )
            )
