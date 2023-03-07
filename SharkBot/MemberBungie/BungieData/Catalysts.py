import discord

from .BungieData import BungieData
import SharkBot

ROOT_NODE = SharkBot.Destiny.Definitions.DestinyPresentationNodeDefinition.get(2744330515)
SUB_NODES = [
    SharkBot.Destiny.Definitions.DestinyPresentationNodeDefinition.get(d["presentationNodeHash"])
    for d in ROOT_NODE["children"]["presentationNodes"]
]

RECORD_NAMES: dict[str, dict[str, str]] = {}
for _node in SUB_NODES:
    _records = {}
    for d in _node["children"]["records"]:
        _record_definition = SharkBot.Destiny.Definitions.DestinyRecordDefinition.get(d["recordHash"])
        _records[str(_record_definition["hash"])] = _record_definition["displayProperties"]["name"]
    RECORD_NAMES[_node["displayProperties"]["name"]] = _records

class Catalysts(BungieData):
    _COMPONENTS = [900]
    _THUMBNAIL_URL = None

    @staticmethod
    def _process_data(data):
        _record_buckets: list[dict[str, dict]] = [
             data["profileRecords"]["data"]["records"]
        ] + [
            _d["records"] for _d in data["characterRecords"]["data"].values()
        ]
        _results: dict[str, dict[str, int]] = {}
        for _node_name, _node_data in RECORD_NAMES.items():
            _node_records: dict[str, int] = {}
            for _record_hash, _record_name in _node_data.items():
                _record_data = None
                for _bucket in _record_buckets:
                    _record_data = _bucket.get(_record_hash)
                    if _record_data is not None:
                        break
                else:
                    continue
                _node_records[_record_name] = _record_data["state"]
            _results[_node_name] = _node_records
        return _results

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
