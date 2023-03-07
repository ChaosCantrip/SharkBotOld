import discord

from .BungieData import BungieData
import SharkBot

ROOT_NODE = SharkBot.Destiny.Definitions.DestinyPresentationNodeDefinition.get(2744330515)
SUB_NODES = [
    SharkBot.Destiny.Definitions.DestinyPresentationNodeDefinition.get(d["presentationNodeHash"])
    for d in ROOT_NODE["children"]["presentationNodes"]
]

RECORD_NAMES: dict[str, dict[int, str]] = {}
for _node in SUB_NODES:
    _records = {}
    for d in _node["children"]["records"]:
        _record_definition = SharkBot.Destiny.Definitions.DestinyRecordDefinition.get(d["recordHash"])
        _records[str(_record_definition["hash"])] = _record_definition["displayProperties"]["name"]
    RECORD_NAMES[_node["displayProperties"]["name"]] = _records

class Catalysts(BungieData):
    _COMPONENTS = []
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
