import discord
from datetime import datetime

from .BungieData import BungieData
import SharkBot

root_node = SharkBot.Destiny.Definitions.DestinyPresentationNodeDefinition.get("3741753466")

child_nodes = [SharkBot.Destiny.Definitions.DestinyPresentationNodeDefinition.get(d["presentationNodeHash"]) for d in root_node["children"]["presentationNodes"]]


class Objective:

    def __init__(self, definition: dict):
        self.name = definition["displayProperties"]["name"]
        self.description = definition["displayProperties"]["description"]
        self.hash = str(definition["hash"])

    def __repr__(self):
        return f"Objective[\n  {self.name}\n  {self.description}\n {self.hash}\n]"

class RecordSet:

    def __init__(self, definition: dict):
        self.name = definition["displayProperties"]["name"]
        self.description = definition["displayProperties"]["description"]
        self.objectives = [Objective(SharkBot.Destiny.Definitions.DestinyRecordDefinition.get(d["recordHash"])) for d in definition["children"]["records"]]

    def __repr__(self):
        return f"RecordSet[\n  {self.name}\n  {self.description}\n  {self.objectives}\n]"

class GuardianRank:

    def __init__(self, number: int, definition: dict):
        self.number = number
        self.name = definition["displayProperties"]["name"]
        self.description = definition["displayProperties"]["description"]
        self.record_sets = [RecordSet(SharkBot.Destiny.Definitions.DestinyPresentationNodeDefinition.get(d["presentationNodeHash"])) for d in definition["children"]["presentationNodes"]]
        self.completion_record_hash = str(definition["completionRecordHash"])

    def __repr__(self):
        return f"GuardianRank[\n  {self.number}\n  {self.name}\n  {self.description}\n  {self.record_sets}\n {self.completion_record_hash}\n]"

GUARDIAN_RANKS = [GuardianRank(i + 1, node) for i, node in enumerate(child_nodes)]

print(GUARDIAN_RANKS[3])

class GuardianRanks(BungieData):
    _COMPONENTS = [200,900,1200]
    _THUMBNAIL_URL = None

    @staticmethod
    def _process_data(data):
        characters = list(data["characters"]["data"].values())
        characters.sort(key=lambda c: datetime.fromisoformat(c["dateLastPlayed"]), reverse=True)
        character_hash = str(characters[0]["characterId"])
        character_records = data["characterRecords"]["data"][character_hash]["records"]
        character_records |= data["profileRecords"]["data"]["records"]

        output = {}
        for rank in GUARDIAN_RANKS:
            rank_data = {
                "completed": character_records[rank.completion_record_hash]["objectives"][0]["complete"],
                "records": {}
            }
            for record_set in rank.record_sets:
                record_set_data = {}
                for objective in record_set.objectives:
                    record_set_data[objective.hash] = {
                        "name": objective.name,
                        "description": objective.description,
                        "completed": character_records[objective.hash]["objectives"][0]["complete"],
                        "completionValue": character_records[objective.hash]["objectives"][0]["completionValue"],
                        "progress": character_records[objective.hash]["objectives"][0]["progress"]
                    }
                rank_data["records"][record_set.name] = record_set_data
            output[f"Rank {rank.number}: {rank.name}"] = rank_data
        return output

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
