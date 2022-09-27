import json

from SharkBot import Destiny
from typing import TypedDict
from datetime import datetime


class _DifficultyData(TypedDict):
    champions: dict[str, int]
    shields: dict[str, int]


class _NightfallData(TypedDict):
    name: str
    destination: str
    legend: _DifficultyData
    master: _DifficultyData


class Nightfall:

    def __init__(self, name: str, destination: str, legend: _DifficultyData, master: _DifficultyData):
        self.name = name
        self.destination = destination
        self.legend = Destiny.LostSector.Difficulty(**legend)
        self.master = Destiny.LostSector.Difficulty(**master)

    @property
    def champion_types(self) -> set[Destiny.Champion.Champion]:
        return set(self.legend.champion_types + self.master.champion_types)

    @property
    def shield_types(self) -> set[Destiny.Shield.Shield]:
        return set(self.legend.shield_types + self.master.shield_types)

    @property
    def champion_list(self) -> str:
        return ", ".join(champion.text for champion in self.champion_types)

    @property
    def shield_list(self) -> str:
        return ", ".join(shield.text for shield in self.shield_types)


with open("data/static/destiny/nightfalls/nightfalls.json", "r") as infile:
    nightfallJsonData: list[_NightfallData] = json.load(infile)

nightfalls = [Nightfall(**nightfallData) for nightfallData in nightfallJsonData]


def get(search: str) -> Nightfall:
    for nightfall in nightfalls:
        if nightfall.name == search:
            return nightfall
    else:
        raise Destiny.Errors.NightfallNotFoundError(search)


with open("data/static/destiny/nightfalls/rotation.json", "r") as infile:
    rotationData: list[str] = json.load(infile)

rotation = [get(nightfallName) for nightfallName in rotationData]
rotationStart = datetime(year=2022, month=8, day=23)
