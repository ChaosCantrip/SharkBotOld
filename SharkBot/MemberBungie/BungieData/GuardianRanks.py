import discord
from datetime import datetime

from .BungieData import BungieData
from ..ProfileResponseData import ProfileResponseData
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
        self.hash = str(definition["hash"])

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

# The Code in here is terrible.
# It's the first time I've used GitHub Copilot, so I was testing it out.
# I'll clean it up later.

class GuardianRanks(BungieData):
    _COMPONENTS = [200,900,1200]
    _THUMBNAIL_URL = None

    @staticmethod
    def _process_data(data: ProfileResponseData):
        characters = list(data["characters"]["data"].values())
        characters.sort(key=lambda c: datetime.fromisoformat(c["dateLastPlayed"]), reverse=True)
        character_hash = str(characters[0]["characterId"])
        character_records = data["characterRecords"]["data"][character_hash]["records"]
        character_records |= data["profileRecords"]["data"]["records"]
        variable_data = data["profileStringVariables"]["data"]["integerValuesByHash"]
        variable_data |= data["characterStringVariables"]["data"][character_hash]["integerValuesByHash"]

        output = {}
        for rank in GUARDIAN_RANKS:
            rank_data = {
                "completed": character_records[rank.completion_record_hash]["objectives"][0]["complete"],
                "record_sets": {}
            }
            for record_set in rank.record_sets:
                record_set_data = {}
                for objective in record_set.objectives:
                    record_set_data[objective.hash] = {
                        "completed": character_records[objective.hash]["objectives"][0]["complete"],
                        "completionValue": character_records[objective.hash]["objectives"][0]["completionValue"],
                        "progress": character_records[objective.hash]["objectives"][0]["progress"]
                    }
                    if "{var:" in objective.description:
                        relevant_variable_hashes = [s.split("}")[0] for s in objective.description.split("{var:") if "}" in s]
                        record_set_data[objective.hash]["variables"] = {
                            variable_hash: variable_data[variable_hash] for variable_hash in relevant_variable_hashes
                        }

                rank_data["record_sets"][record_set.hash] = {
                    "completed": all(r["completed"] for r in record_set_data.values()),
                    "records": record_set_data
                }
            output[rank.completion_record_hash] = rank_data
        print(SharkBot.Utils.JSON.dumps(output, indent=2))
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

    @staticmethod
    def _format_embed_data(embed: discord.Embed, data, **kwargs):
        previous_rank = None
        for rank in GUARDIAN_RANKS:
            if data[rank.completion_record_hash]["completed"]:
                previous_rank = rank
                continue
            else:
                break
        else:
            rank = GUARDIAN_RANKS[-1]
            embed.title = f"Guardian Rank {rank.number} - {rank.name}"
            embed.description = "You have completed all Guardian Ranks!"
            return
        rank_data = data[rank.completion_record_hash]
        embed.title = f"Guardian Rank {previous_rank.number} - {previous_rank.name}"
        embed.description = rank.description
        for record_set in rank.record_sets:
            record_set_data = rank_data["record_sets"][record_set.hash]
            if record_set_data["completed"]:
                continue
            for objective in record_set.objectives:
                objective_data = record_set_data["records"][objective.hash]
                if objective_data["completed"]:
                    continue
                if "{var:" in objective.description:
                    description = objective.description
                    for variable_hash, variable_value in objective_data["variables"].items():
                        description = description.replace(f"{{var:{variable_hash}}}", f"{variable_value:,}")
                else:
                    description = objective.description
                embed.add_field(
                    name=f"{record_set.name} | {objective.name} ({objective_data['progress']}/{objective_data['completionValue']})",
                    value=description.split("\n")[0],
                    inline=False
                )
