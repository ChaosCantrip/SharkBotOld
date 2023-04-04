import discord

from .BungieData import BungieData
import SharkBot


class Item:

    def __init__(self, item_hash: int):
        self.definition: dict = SharkBot.Destiny.Definitions.DestinyInventoryItemDefinition.get(item_hash)
        self.name: str = self.definition["displayProperties"]["name"]
        self.hash: int = item_hash

    def __repr__(self):
        return f"Item[{self.hash}] {self.name}"


class ItemCategory:

    def __init__(self, category_hash: int):
        self.definition: dict = SharkBot.Destiny.Definitions.DestinyInventoryItemDefinition.get(category_hash)
        self.name: str = self.definition["displayProperties"]["name"]
        self.items = [
            Item(item["itemHash"]) for item in self.definition["preview"]["derivedItemCategories"][0]["items"]
        ]
        self.hash: int = category_hash

    def __repr__(self):
        return f"ItemCategory[{self.hash}] {self.name}\n" + "\n".join([f"    {item}" for item in self.items])


class CollectibleState:

    def __init__(self, state_num: int):
        self.state_map = bin(state_num)
        self.NONE = self.state_map[-1] == "1"
        self.NOT_ACQUIRED = self.state_map[-2] == "1"
        self.OBSCURED = self.state_map[-3] == "1"
        self.INVISIBLE = self.state_map[-4] == "1"
        self.CANNOT_AFFORD_MATERIALS = self.state_map[-5] == "1"
        self.INVENTORY_SPACE_UNAVAILABLE = self.state_map[-6] == "1"
        self.UNIQUENESS_VIOLATION = self.state_map[-7] == "1"
        self.PURCHASE_DISABLED = self.state_map[-8] == "1"


_MONUMENT_DEFINITION = SharkBot.Destiny.Definitions.DestinyVendorDefinition.get(4230408743)
_VENDOR_ITEMS = [ItemCategory(item["itemHash"]) for item in _MONUMENT_DEFINITION["itemList"]]


class Monument(BungieData):
    _COMPONENTS = [SharkBot.Destiny.Enums.ComponentType.Collectibles]
    _THUMBNAIL_URL = None

    # @staticmethod
    # def _process_data(data):
    #     return data

    # @staticmethod
    # def _process_cache_write(data):
    #     return data

    # @staticmethod
    # def _process_cache_load(data):
    #     return data

    # @classmethod
    # def _format_cache_embed_data(cls, embed: discord.Embed, data, **kwargs):
    #     cls._format_embed_data(embed, data)

    # @staticmethod
    # def _format_embed_data(embed: discord.Embed, data, **kwargs):
    #     embed.description = f"\n```{SharkBot.Utils.JSON.dumps(data)}```"
