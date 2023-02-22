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
    objectives: list[ObjectiveResponseData]
    intervalsRedeemedCount: int

    def __post_init__(self):
        objective_data: dict
        self.objectives = [ObjectiveResponseData(**objective_data) for objective_data in self.objectives]


# Data Imports

SEAL_HASHES: dict[str, str] = SharkBot.Utils.JSON.load("data/static/bungie/definitions/SealHashes.json")
SEAL_DEFINITIONS: dict[str, SealData] = {
    seal_hash: SealData(**seal_data) for seal_hash, seal_data in SharkBot.Utils.JSON.load("data/static/bungie/definitions/SealDefinitions.json").items()
}


# Class Definition

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
