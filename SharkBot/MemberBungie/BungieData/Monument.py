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


_MONUMENT_DEFINITION = SharkBot.Destiny.Definitions.DestinyVendorDefinition.get(4230408743)
_VENDOR_ITEMS = [ItemCategory(item["itemHash"]) for item in _MONUMENT_DEFINITION["itemList"]]


class Monument(BungieData):
    _THUMBNAIL_URL = None

    async def fetch_data(self, write_cache: bool = True):
        data = await self.member.bungie.get_profile_response(*self._COMPONENTS)
        data = self._process_data(data)
        if write_cache:
            self.write_cache(data)
        return data

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
