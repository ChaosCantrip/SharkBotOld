import json

from SharkBot import Destiny
from typing import TypedDict


class _DifficultyData(TypedDict):
    champions: dict[str, int]
    shields: dict[str, int]


class _NightfallData(TypedDict):
    name: str
    destination: str
    legend: _DifficultyData
    master: _DifficultyData


class Nightfall:
    nightfalls = []
    rotation = []

    def __init__(self, name: str, destination: str, legend: _DifficultyData, master: _DifficultyData):
        self.name = name
        self.destination = destination
        self.legend = Destiny.Difficulty(**legend)
        self.master = Destiny.Difficulty(**master)

    @property
    def champion_types(self) -> set[Destiny.Champion]:
        return set(self.legend.champion_types + self.master.champion_types)

    @property
    def shield_types(self) -> set[Destiny.Shield]:
        return set(self.legend.shield_types + self.master.shield_types)

    @property
    def gm_icons(self) -> str:
        return " ".join([" ".join([e.icon for e in g]) for g in [self.master.champion_types, self.master.shield_types]])

    @property
    def champion_list(self) -> str:
        return ", ".join(str(champion) for champion in self.champion_types)

    @property
    def shield_list(self) -> str:
        return ", ".join(str(shield) for shield in self.shield_types)

    @classmethod
    def get(cls, search: str):
        search = search.lower()
        for nightfall in cls.nightfalls:
            if nightfall.name.lower() == search:
                return nightfall
        else:
            raise Destiny.Errors.NightfallNotFoundError(search)

    @classmethod
    def get_current(cls):
        return cls.rotation[Destiny.get_week_index() % len(cls.rotation)]

    @classmethod
    def rotation_from(cls, nightfall) -> list:
        start_index = cls.rotation.index(nightfall)
        cycle = cls.rotation[start_index:] + cls.rotation[:start_index]
        cycle = cycle[1:] + [cycle[0]]
        return cycle


with open("data/static/destiny/nightfalls/nightfalls.json", "r") as infile:
    nightfallJsonData: list[_NightfallData] = json.load(infile)

Nightfall.nightfalls = [Nightfall(**nightfallData) for nightfallData in nightfallJsonData]


with open("data/static/destiny/nightfalls/rotation.json", "r") as infile:
    rotation_data: list[str] = json.load(infile)

for nightfall in rotation_data:
    if nightfall is None:
        Nightfall.rotation.append(None)
    else:
        Nightfall.rotation.append(Nightfall.get(nightfall))
