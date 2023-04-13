import discord

from .BungieData import BungieData
from ..ProfileResponseData import ProfileResponseData
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
        self.objectives: dict[str, _Objective] = {
            str(objective.hash): objective for objective in
            [_Objective(objective_hash) for objective_hash in self.definition["objectiveHashes"]]
        }


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
        self.records: dict[str, _Record] = {
            str(record.hash): record for record in
            [_Record(record["recordHash"]) for record in self.definition["children"]["records"]]
        }


root_node_definition = SharkBot.Destiny.Definitions.DestinyPresentationNodeDefinition.get(616318467)
SEALS: dict[str, _Seal] = {
    str(seal.hash): seal for seal in
    [_Seal(seal["presentationNodeHash"]) for seal in root_node_definition["children"]["presentationNodes"]]
}


class Seals(BungieData):
    _COMPONENTS = [900]
    _THUMBNAIL_URL = None

    @staticmethod
    def _process_data(data: ProfileResponseData):
        records: dict[str, dict] = data["profileRecords"]["data"]["records"]
        records |= list(data["characterRecords"]["data"].values())[0]["records"]
        results: dict[str, dict[str, str | dict[str, bool | int]]] = {}
        for seal_hash, seal_definition in SEALS.items():
            seal_results = {}
            for record_hash, record_definition in seal_definition.records.items():
                print("\nRECORD")
                print(record_hash)
                record_data = records[record_hash]
                record_results = {}
                objectives_data: list[dict] = record_data.get("objectives", [])
                objectives_data.extend(record_data.get("intervalObjectives", []))
                for objective_data in objectives_data:
                    record_results[str(objective_data["objectiveHash"])] = {
                        "complete": objective_data["complete"],
                        "progress": objective_data["progress"],
                        "completionValue": objective_data["completionValue"]
                    }
                seal_results[record_hash] = {
                    "complete": all([objective_data["complete"] for objective_data in record_results.values()]),
                    "objectives": record_results
                }
            results[seal_hash] = {
                "complete": all([record_data["complete"] for record_data in seal_results.values()]),
                "records": seal_results
            }
        return results

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
        seal_definition = SEALS[kwargs["seal_hash"]]
        seal_data = data[kwargs["seal_hash"]]
        embed.title = f"{seal_definition.name} Seal"
        if seal_definition.title != seal_definition.name:
            embed.title += f" ({seal_definition.title})"
        embed.set_thumbnail(url=seal_definition.icon)
        output_text: list[str] = [seal_definition.description, ""]
        if seal_data["complete"]:
            output_text.append("Seal Complete")
        else:
            output_text.append("Seal Incomplete")
            for record_hash, record_definition in seal_definition.records.items():
                if seal_data["records"][record_hash]["complete"]:
                    continue
                output_text.append(f"\n**{record_definition.name}**")
                output_text.append(record_definition.description)
                for objective_hash, objective_definition in record_definition.objectives.items():
                    objective_data = seal_data["records"][record_hash]["objectives"][objective_hash]
                    output_text.append(f"`{objective_definition.description}: {objective_data['progress']}/{objective_data['completionValue']}`")
        embed.description = "\n".join(output_text)

