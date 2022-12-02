import json
from typing import TypedDict

from SharkBot import Destiny


class _DungeonData(TypedDict):
    name: str
    destination: str


class _RotationData(TypedDict):
    seasonal: str
    featured: list[str]


class Dungeon:
    dungeons = []
    rotation = []
    seasonal = None

    def __init__(self, name: str, destination: str) -> None:
        self.name = name
        self.destination = destination

    @classmethod
    def get(cls, search: str):
        for dungeon in cls.dungeons:
            if dungeon.name == search:
                return dungeon
        else:
            raise Destiny.Errors.DungeonNotFoundError(search)

    @classmethod
    def get_current(cls):
        return cls.rotation[Destiny.get_week_index() % len(cls.rotation)]


with open("data/static/destiny/dungeons/dungeons.json", "r") as infile:
    dungeonData: list[_DungeonData] = json.load(infile)

Dungeon.dungeons = [Dungeon(**data) for data in dungeonData]


with open("data/static/destiny/dungeons/rotation.json", "r") as infile:
    rotationData: _RotationData = json.load(infile)

Dungeon.seasonal = Dungeon.get(rotationData["seasonal"])
Dungeon.rotation = [Dungeon.get(dungeonName) for dungeonName in rotationData["featured"]]
