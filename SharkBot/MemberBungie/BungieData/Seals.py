from dataclasses import dataclass
from typing import Union

import discord

from .BungieData import BungieData
import SharkBot

# Data Classes

@dataclass
class ObjectiveData:
    description: str
    completionValue: int

@dataclass
class RecordData:
    name: str
    description: str
    objectives: dict[str, ObjectiveData]
    forTitleGilding: bool

    def __post_init__(self):
        objective_data: dict
        self.objectives = {objective_hash: ObjectiveData(**objective_data) for objective_hash, objective_data in self.objectives.items()}

@dataclass
class SealData:
    name: str
    description: str
    icon: str
    records: dict[str, RecordData]
    completionRecordHash: int
    title: str

    def __post_init__(self):
        record_data: dict
        self.records = {record_hash: RecordData(**record_data) for record_hash, record_data in self.records.items()}

@dataclass
class ObjectiveResponseData:
    objectiveHash: int
    progress: int
    completionValue: int
    complete: bool
    visible: bool

@dataclass
class RecordResponseData:
    objectives: dict[str, ObjectiveResponseData]

    def __post_init__(self):
        objective_data: dict
        self.objectives = {str(objective_data["objectiveHash"]): ObjectiveResponseData(**objective_data) for objective_data in self.objectives}

@dataclass
class ProcessedObjectiveData:
    description: str
    progress: int
    completionValue: int
    complete: bool

    @property
    def printout(self) -> str:
        return f"{self.description} - {self.progress}/{self.completionValue}"

    @property
    def raw_data(self) -> dict:
        return dict(self.__dict__)

@dataclass
class ProcessedRecordData:
    name: str
    description: str
    objectives: list[ProcessedObjectiveData]
    complete: bool

    @property
    def field_data(self) -> dict:
        return {
            "name": self.name,
            "value": f"**{self.description}**\n" + "\n\n".join(o.printout for o in self.objectives)
        }

    @property
    def raw_data(self) -> dict:
        _raw_data = dict(self.__dict__)
        _raw_data["objectives"] = [o.raw_data for o in self.objectives]
        return _raw_data

@dataclass
class ProcessedSealData:
    name: str
    description: str
    icon: str
    records: list[ProcessedRecordData]
    title: str

    @property
    def raw_data(self) -> dict:
        _raw_data = dict(self.__dict__)
        _raw_data["records"] = [r.raw_data for r in self.records]
        return _raw_data


# Data Imports

SEAL_HASHES: dict[str, str] = SharkBot.Utils.JSON.load("data/static/bungie/definitions/SealHashes.json")
SEAL_DEFINITIONS: dict[str, SealData] = {
    seal_hash: SealData(**seal_data) for seal_hash, seal_data in SharkBot.Utils.JSON.load("data/static/bungie/definitions/SealDefinitions.json").items()
}

a = ObjectiveData(
    description="Test",
    completionValue=1
)

# Class Definition

class Seals(BungieData):
    _COMPONENTS = [900]
    _THUMBNAIL_URL = None

    @staticmethod
    def _process_data(data) -> dict[str, ProcessedSealData]:
        response_data = data["profileRecords"]["data"]["records"]
        for character_data in data["characterRecords"]["data"].values():
            response_data |= character_data["records"]
        result_data: dict[str, ProcessedSealData] = {}
        for seal_hash, seal_data in SEAL_DEFINITIONS.items():
            records: list[ProcessedRecordData] = []
            for record_hash, record_data in seal_data.records.items():
                record_response_data = response_data[record_hash]
                record_response = RecordResponseData(
                    objectives=record_response_data.get("objectives", []) + record_response_data.get("intervalObjectives", [])
                )
                objectives: list[ProcessedObjectiveData] = []
                for objective_hash, objective_definition in record_data.objectives.items():
                    objective_data = record_response.objectives[objective_hash]
                    objectives.append(
                        ProcessedObjectiveData(
                            description=objective_definition.description,
                            progress=objective_data.progress,
                            completionValue=objective_data.completionValue,
                            complete=objective_data.complete
                        )
                    )
                records.append(
                    ProcessedRecordData(
                        name=record_data.name,
                        description=record_data.description,
                        objectives=objectives,
                        complete=all([objective.complete for objective in objectives])
                    )
                )
            result_data[seal_hash] = ProcessedSealData(
                name=seal_data.name,
                description=seal_data.description,
                icon=seal_data.icon,
                records=records,
                title=seal_data.title
            )
        return result_data

    @staticmethod
    def _process_cache_write(data: dict[str, ProcessedSealData]):
        return {seal_hash: seal_data.raw_data for seal_hash, seal_data in data.items()}

    @staticmethod
    def _process_cache_load(data: dict[str, dict]):
        return {seal_hash: ProcessedSealData(**seal_data) for seal_hash, seal_data in data.items()}

    # @classmethod
    # def _format_cache_embed_data(cls, embed: discord.Embed, data, **kwargs):
    #     cls._format_embed_data(embed, data)

    @staticmethod
    def _format_embed_data(embed: discord.Embed, data: dict[str, ProcessedSealData], seal_hash: str = None, **kwargs):
        seal_data = data[seal_hash]
        embed.title = f"{seal_data.name} - `{seal_data.title}`"
        embed.description = seal_data.description
        embed.set_thumbnail(url=seal_data.icon)
        for record in seal_data.records:
            embed.add_field(**record.field_data)

