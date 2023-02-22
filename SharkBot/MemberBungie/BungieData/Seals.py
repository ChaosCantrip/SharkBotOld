from typing import TypedDict

import discord

from .BungieData import BungieData
import SharkBot

# Data Classes

class ObjectiveData(TypedDict):
    description: str
    completionValue: int

class RecordData(TypedDict):
    name: str
    description: str
    objectives: dict[str, ObjectiveData]
    forTitleGilding: bool

class SealData(TypedDict):
    name: str
    description: str
    icon: str
    records: dict[str, RecordData]
    completionRecordHash: int
    title: str

class ObjectiveResponseData(TypedDict):
    objectiveHash: int
    progress: int
    completionValue: int
    complete: bool
    visible: bool

class RecordResponseData(TypedDict):
    state: int
    objectives: list[ObjectiveResponseData]
    intervalsRedeemedCount: int


# Data Imports

SEAL_HASHES: dict[str, str] = SharkBot.Utils.JSON.load("data/static/bungie/definitions/SealHashes.json")
SEAL_DEFINITIONS: dict[str, SealData] = SharkBot.Utils.JSON.load("data/static/bungie/definitions/SealDefinitions.json")


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
