from dataclasses import dataclass

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

@dataclass
class SealData:
    name: str
    description: str
    icon: str
    records: dict[str, RecordData]
    completionRecordHash: int
    title: str

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


# Data Imports

SEAL_HASHES: dict[str, str] = SharkBot.Utils.JSON.load("data/static/bungie/definitions/SealHashes.json")
SEAL_DEFINITIONS: dict[str, SealData] = {
    seal_hash: SealData(
        name=seal_data["name"],
        description=seal_data["description"],
        icon=seal_data["icon"],
        records={
            record_hash: RecordData(
                name=record_data["name"],
                description=record_data["description"],
                objectives={
                    objective_hash: ObjectiveData(
                        description=objective_data["description"],
                        completionValue=objective_data["completionValue"]
                    ) for objective_hash, objective_data in record_data["objectives"].items()
                },
                forTitleGilding=record_data["forTitleGilding"]
            ) for record_hash, record_data in seal_data["records"].items()
        },
        completionRecordHash=seal_data["completionRecordHash"],
        title=seal_data["title"]
    ) for seal_hash, seal_data in SharkBot.Utils.JSON.load("data/static/bungie/definitions/SealDefinitions.json").items()
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
