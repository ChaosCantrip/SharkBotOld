from dataclasses import dataclass
from typing import Optional, Callable

from .BungieData import BungieData
import SharkBot
import discord

_data = SharkBot.Utils.JSON.load("data/static/bungie/definitions/LevelObjectiveHashes.json")
_WEAPON_LEVEL_RECORDS: list[str] = _data["records"]
_LEVEL_OBJECTIVE_HASH: int = _data["objective"]

@dataclass
class CraftedWeapon:
    name: str
    level: int
    type: str

    @property
    def raw_data(self) -> dict:
        return {"name": self.name, "level": self.level, "type": self.type}


class WeaponLevels(BungieData):
    _COMPONENTS = [102,201,205,309]
    _THUMBNAIL_URL = "https://www.bungie.net/common/destiny2_content/icons/e7e6d522d375dfa6dec055135ce6a77e.png"
    _EMBED_TITLE = "Weapon Levels"

    @staticmethod
    def _process_data(data) -> list[CraftedWeapon]:
        item_components: dict[str, dict] = data["itemComponents"]["plugObjectives"]["data"]
        items: list[dict] = list(item for item in data["profileInventory"]["data"]["items"] if "itemInstanceId" in item)
        for bucket in ["characterInventories", "characterEquipment"]:
            bucket_data: dict[str, dict[str, list[dict]]] = data[bucket]["data"]
            for item_set in bucket_data.values():
                items.extend(item for item in item_set["items"] if item.get("itemInstanceId") is not None)

        weapons_with_levels: list[CraftedWeapon] = []

        for item in items:
            if (item_instance:=item_components.get(item["itemInstanceId"])) is None:
                continue
            item_objectives: dict[str, list] = item_instance["objectivesPerPlug"]
            shaped_record = None
            for record_hash in _WEAPON_LEVEL_RECORDS:
                shaped_record = item_objectives.get(record_hash)
                if shaped_record is not None:
                    break
            if shaped_record is not None:
                item_definition = SharkBot.Destiny.Definitions.DestinyInventoryItemDefinition.get(item["itemHash"])
                item_name = item_definition["displayProperties"]["name"]
                level_record = [record for record in shaped_record if record["objectiveHash"] == _LEVEL_OBJECTIVE_HASH][0]
                item_type = SharkBot.Destiny.Enums.AmmoType(item_definition["equippingBlock"]["ammoType"]).name.title() + " Weapons"
                weapons_with_levels.append(CraftedWeapon(item_name, level_record["progress"], item_type))

        return weapons_with_levels

    @staticmethod
    def _process_cache_write(data: list[CraftedWeapon]) -> list[dict]:
        return [weapon.raw_data for weapon in data]

    @staticmethod
    def _process_cache_load(data: list[dict]) -> list[CraftedWeapon]:
        return [CraftedWeapon(**weapon) for weapon in data]

    @staticmethod
    def _format_embed_data(embed: discord.Embed, data: list[CraftedWeapon], f: Optional[Callable[[CraftedWeapon], bool]] = None, **kwargs):
        sorted_data = sorted(data, key=lambda x:x.level)
        if f is not None:
            sorted_data = list(filter(f, sorted_data))

        for weapon_type in ["Primary Weapons", "Special Weapons", "Heavy Weapons"]:
            weapons_of_type = [weapon for weapon in sorted_data if weapon.type == weapon_type]
            if len(weapons_of_type) > 0:
                embed.add_field(
                    name=f"__{weapon_type}__",
                    value="\n".join(f"`{weapon.level}` {weapon.name}" for weapon in weapons_of_type),
                    inline=False
                )
            else:
                embed.add_field(
                    name=f"__{weapon_type}__",
                    value="There's nothing here!",
                    inline=False
                )

        total_level = sum(weapon.level for weapon in sorted_data)
        embed.set_footer(text=f"Total Weapon Levels: {total_level:,}")