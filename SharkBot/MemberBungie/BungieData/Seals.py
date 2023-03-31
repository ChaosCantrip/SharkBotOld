import discord

from .BungieData import BungieData
import SharkBot


class _Objective:

    def __init__(self, objective_hash: int):
        self.hash = objective_hash
        self.definition = SharkBot.Destiny.Definitions.DestinyObjectiveDefinition.get(objective_hash)
        if (progress_description := self.definition["progressDescription"]) != "":
            self.description = progress_description
        else:
            self.description = "Objective"
        self.completion_value = self.definition["completionValue"]


class _Record:

    def __init__(self, record_hash: int):
        self.hash = record_hash
        self.definition = SharkBot.Destiny.Definitions.DestinyRecordDefinition.get(record_hash)
        self.name = self.definition["displayProperties"]["name"]
        self.description = self.definition["displayProperties"]["description"]
        self.objectives = [_Objective(objective_hash) for objective_hash in self.definition["objectiveHashes"]]


class _Seal:

    def __init__(self, presentation_node_hash: int):
        self.hash = presentation_node_hash
        self.definition = SharkBot.Destiny.Definitions.DestinyPresentationNodeDefinition.get(presentation_node_hash)
        self.name = self.definition["displayProperties"]["name"]
        self.description = self.definition["displayProperties"]["description"]
        self.icon = f"https://bungie.net{self.definition['displayProperties']['icon']}"
        self.completion_record_hash = self.definition["completionRecordHash"]
        self.completion_record = SharkBot.Destiny.Definitions.DestinyRecordDefinition.get(self.completion_record_hash)
        if self.completion_record["titleInfo"]["hasTitle"]:
            self.title = self.completion_record["titleInfo"]["titlesByGender"]["Male"]
        else:
            self.title = self.name
        self.records = [_Record(record["recordHash"]) for record in self.definition["children"]["records"]]


root_node_definition = SharkBot.Destiny.Definitions.DestinyPresentationNodeDefinition.get(616318467)
seals = [_Seal(child["presentationNodeHash"]) for child in root_node_definition["children"]["presentationNodes"]]


class Seals(BungieData):
    _COMPONENTS = [900]
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
