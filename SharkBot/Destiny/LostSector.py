import json
import datetime
from typing import TypedDict
from SharkBot.Destiny import Champion, Shield, Errors as DestinyErrors


class _DifficultyData(TypedDict):
    champions: dict[str, int]
    shields: dict[str, int]


class _LostSectorData(TypedDict):
    name: str
    destination: str
    burn: str
    embed_url: str
    legend: _DifficultyData
    master: _DifficultyData


class LostSector:

    def __init__(self, name: str, destination: str, burn: str, embed_url: str,
                 legend: _DifficultyData, master: _DifficultyData) -> None:
        self.name = name
        self.destination = destination
        self.burn = Shield.get(burn)
        self.embed_url = embed_url
        self.legend = Difficulty(**legend)
        self.master = Difficulty(**master)

    @property
    def champion_types(self) -> set[Champion.Champion]:
        return set(self.legend.champion_types + self.master.champion_types)

    @property
    def shield_types(self) -> set[Shield.Shield]:
        return set(self.legend.shield_types + self.master.shield_types)

    @property
    def champion_list(self) -> str:
        return ", ".join(champion for champion in self.champion_types)

    @property
    def shield_list(self) -> str:
        return ", ".join(shield for shield in self.shield_types)


class Difficulty:

    def __init__(self, champions: dict[str, int], shields: dict[str, int]) -> None:
        self.champions = {Champion.get(champion): number for champion, number in champions.items()}
        self.shields = {Shield.get(shield): number for shield, number in shields.items()}

    @property
    def champion_types(self) -> list[Champion.Champion]:
        return list(self.champions.keys())

    @property
    def shield_types(self) -> list[Shield.Shield]:
        return list(self.shields.keys())

    @property
    def champion_list(self) -> str:
        return "\n".join(f"{champion} x{number}" for champion, number in self.champions.items())

    @property
    def shield_list(self) -> str:
        return "\n".join(f"{shield} x{number}" for shield, number in self.shields.items())

    @property
    def details(self) -> str:
        return f"{self.champion_list}\n{self.shield_list}"


with open("data/static/destiny/lost_sectors/lost_sectors.json", "r") as infile:
    lostSectorData: list[_LostSectorData] = json.load(infile)

lostSectors = [LostSector(**data) for data in lostSectorData]
rotationStart = datetime.datetime(2022, 9, 13)
resetTime = datetime.time(18)


def get(search: str) -> LostSector:
    for lostSector in lostSectors:
        if lostSector.name == search:
            return lostSector
    else:
        raise DestinyErrors.LostSectorNotFoundError(search)


with open("data/static/destiny/lost_sectors/rotation.json") as infile:
    rotationData = json.load(infile)

rotation = [get(sectorName) for sectorName in rotationData]


def get_current() -> LostSector:
    dtnow = datetime.datetime.now()
    if dtnow.time() < resetTime:
        dtnow = dtnow - datetime.timedelta(days=1)
    days = (dtnow - rotationStart).days
    position = days % len(rotation)
    return rotation[position]
