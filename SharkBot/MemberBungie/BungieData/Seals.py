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
    state: int
    objectives: dict[str, ObjectiveResponseData]
    intervalsRedeemedCount: int

    def __post_init__(self):
        objective_data: dict
        self.objectives = {str(objective_data["objectiveHash"]): ObjectiveResponseData(**objective_data) for objective_data in self.objectives}

@dataclass
class ProcessedObjectiveData:
    description: str
    progress: int
    completionValue: int
    complete: bool

@dataclass
class ProcessedRecordData:
    name: str
    description: str
    objectives: list[ProcessedObjectiveData]
    complete: bool

@dataclass
class ProcessedSealData:
    name: str
    description: str
    icon: str
    records: list[ProcessedRecordData]
    title: str


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
        result_data: dict[str, ProcessedSealData] = {}
        for seal_hash, seal_data in SEAL_DEFINITIONS.items():
            records: list[ProcessedRecordData] = []
            for record_hash, record_data in seal_data.records.items():
                record_response = RecordResponseData(**response_data[record_hash])
                objectives: list[ProcessedObjectiveData] = []
                for objective_hash, objective_data in record_response.objectives.items():
                    objective_definition = record_data.objectives[objective_hash]
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
