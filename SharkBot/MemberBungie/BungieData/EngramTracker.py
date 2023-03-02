from typing import Optional

import discord

from .BungieData import BungieData
import SharkBot

_ENGRAM_TRACKER_HASH = 1624697519
_ENGRAM_TRACKER_DEFINITION = SharkBot.Destiny.Definitions.DestinyInventoryItemDefinition.get(_ENGRAM_TRACKER_HASH)
_engram_tracker_description_lines = _ENGRAM_TRACKER_DEFINITION["displayProperties"]["description"].split("\n")[1:]
_ENGRAM_TRACKER_VARIABLES: dict[str, str] = {
    d[0]: d[1][5:-1] for d in [
        s.split(": ") for s in _engram_tracker_description_lines
    ]
}
_ENGRAM_TRACKER_ICON: Optional[str] = None
if _ENGRAM_TRACKER_DEFINITION["displayProperties"]["hasIcon"]:
    _ENGRAM_TRACKER_ICON = "https://bungie.net" + _ENGRAM_TRACKER_DEFINITION["displayProperties"]["icon"]

class EngramTracker(BungieData):
    _COMPONENTS = []
    _THUMBNAIL_URL = _ENGRAM_TRACKER_ICON

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
