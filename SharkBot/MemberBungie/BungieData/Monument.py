import discord

from .BungieData import BungieData
import SharkBot

_ignored_hashes = [
    897074661,  # Forsaken Cipher
    2832451056,  # Legacy Gear
    4257549985  # Ascendant Shard
]


class Item:

    def __init__(self, item_hash: int):
        self.definition: dict = SharkBot.Destiny.Definitions.DestinyInventoryItemDefinition.get(item_hash)
        self.name: str = self.definition["displayProperties"]["name"]
        self.hash: int = self.definition["collectibleHash"]

    def __repr__(self):
        return f"Item[{self.hash}] {self.name}"


class ItemCategory:

    def __init__(self, category_hash: int):
        self.definition: dict = SharkBot.Destiny.Definitions.DestinyInventoryItemDefinition.get(category_hash)
        self.name: str = self.definition["displayProperties"]["name"]
        self.items = [
            Item(item["itemHash"]) for item in self.definition["preview"]["derivedItemCategories"][0]["items"] if item["itemHash"] not in _ignored_hashes
        ]
        self.hash: int = category_hash

    def __repr__(self):
        return f"ItemCategory[{self.hash}] {self.name}\n" + "\n".join([f"    {item}" for item in self.items])


class CollectibleState:

    def __init__(self, state_num: int):
        self.state_num = state_num
        self.state_map = bin(state_num)
        self.NONE = bool(state_num & 0b0)
        self.NOT_ACQUIRED = bool(state_num & 0b1)
        self.OBSCURED = bool(state_num & 0b10)
        self.INVISIBLE = bool(state_num & 0b100)
        self.CANNOT_AFFORD_MATERIALS = bool(state_num & 0b1000)
        self.INVENTORY_SPACE_UNAVAILABLE = bool(state_num & 0b10000)
        self.UNIQUENESS_VIOLATION = bool(state_num & 0b100000)
        self.PURCHASE_DISABLED = bool(state_num & 0b1000000)


_MONUMENT_DEFINITION = SharkBot.Destiny.Definitions.DestinyVendorDefinition.get(4230408743)
_VENDOR_ITEMS = [ItemCategory(item["itemHash"]) for item in _MONUMENT_DEFINITION["itemList"] if item["itemHash"] not in _ignored_hashes]


class Monument(BungieData):
    _COMPONENTS = [SharkBot.Destiny.Enums.ComponentType.Collectibles.value]
    _THUMBNAIL_URL = None

    @staticmethod
    def _process_data(data) -> dict[str, dict[str, CollectibleState]]:
        collectibles_data: dict[str, dict] = data["profileCollectibles"]["data"]["collectibles"]
        for character_data in data["characterCollectibles"]["data"].values():
            collectibles_data |= character_data["collectibles"]
        results: dict[str, dict[str, CollectibleState]] = {}
        for category in _VENDOR_ITEMS:
            results[category.name] = {}
            for item in category.items:
                results[category.name][item.name] = CollectibleState(collectibles_data[str(item.hash)]["state"])
        return results

    @staticmethod
    def _process_cache_write(data: dict[str, dict[str, CollectibleState]]) -> dict[str, dict[str, int]]:
        return {
            category_name: {
                item_name: item_state.state_num for item_name, item_state in category_data.items()
            } for category_name, category_data in data.items()
        }

    @staticmethod
    def _process_cache_load(data: dict[str, dict[str, int]]) -> dict[str, dict[str, CollectibleState]]:
        return {
            category_name: {
                item_name: CollectibleState(item_state) for item_name, item_state in category_data.items()
            } for category_name, category_data in data.items()
        }

    # @classmethod
    # def _format_cache_embed_data(cls, embed: discord.Embed, data, **kwargs):
    #     cls._format_embed_data(embed, data)

    # @staticmethod
    # def _format_embed_data(embed: discord.Embed, data, **kwargs):
    #     embed.description = f"\n```{SharkBot.Utils.JSON.dumps(data)}```"
