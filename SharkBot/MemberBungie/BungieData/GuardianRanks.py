import discord

from .BungieData import BungieData
import SharkBot

root_node = SharkBot.Destiny.Definitions.DestinyPresentationNodeDefinition.get("3741753466")

child_nodes = [SharkBot.Destiny.Definitions.DestinyPresentationNodeDefinition.get(d["presentationNodeHash"]) for d in root_node["children"]["presentationNodes"]]


class Record:

    def __init__(self, definition: dict):
        self.name = definition["displayProperties"]["name"]
        self.description = definition["displayProperties"]["description"]
        self.completion_value: int = SharkBot.Destiny.Definitions.DestinyObjectiveDefinition.get(definition["objectiveHashes"][0])["completionValue"]

    def __repr__(self):
        return f"Record[\n  {self.name}\n  {self.description}\n  {self.completion_value}\n]"

class RecordSet:

    def __init__(self, definition: dict):
        self.name = definition["displayProperties"]["name"]
        self.description = definition["displayProperties"]["description"]
        self.records = [Record(SharkBot.Destiny.Definitions.DestinyRecordDefinition.get(d["recordHash"])) for d in definition["children"]["records"]]

    def __repr__(self):
        return f"RecordSet[\n  {self.name}\n  {self.description}\n  {self.records}\n]"

class GuardianRank:

    def __init__(self, number: int, definition: dict):
        self.number = number
        self.name = definition["displayProperties"]["name"]
        self.description = definition["displayProperties"]["description"]
        self.record_sets = [RecordSet(SharkBot.Destiny.Definitions.DestinyPresentationNodeDefinition.get(d["presentationNodeHash"])) for d in definition["children"]["presentationNodes"]]
        self.completion_record_hash = definition["completionRecordHash"]

    def __repr__(self):
        return f"GuardianRank[\n  {self.number}\n  {self.name}\n  {self.description}\n  {self.record_sets}\n]"

GUARDIAN_RANKS = [GuardianRank(i + 1, node) for i, node in enumerate(child_nodes)]

class GuardianRanks(BungieData):
    _COMPONENTS = [104,1200]
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
