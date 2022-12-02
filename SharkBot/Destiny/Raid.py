import json
from typing import TypedDict

from SharkBot import Destiny


class _RaidData(TypedDict):
    name: str


class _RotationData(TypedDict):
    seasonal: str
    featured: list[str]


class Raid:
    raids = []
    rotation = []
    seasonal = None

    def __init__(self, name: str) -> None:
        self.name = name

    @classmethod
    def get(cls, search: str):
        for raid in cls.raids:
            if raid.name == search:
                return raid
        else:
            raise Destiny.Errors.RaidNotFoundError(search)

    @classmethod
    def get_current(cls):
        return cls.rotation[Destiny.get_week_index() % len(cls.rotation)]


with open("data/static/destiny/raids/raids.json", "r") as infile:
    raidData: list[_RaidData] = json.load(infile)

Raid.raids = [Raid(**data) for data in raidData]


with open("data/static/destiny/raids/rotation.json", "r") as infile:
    rotationData: _RotationData = json.load(infile)

Raid.seasonal = Raid.get(rotationData["seasonal"])
Raid.rotation = [Raid.get(raidName) for raidName in rotationData["featured"]]
