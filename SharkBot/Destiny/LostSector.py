import json
from typing import TypedDict
from SharkBot import Destiny


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
    lost_sectors = []
    rotation = []

    def __init__(self, name: str, destination: str, burn: str, embed_url: str,
                 legend: _DifficultyData, master: _DifficultyData) -> None:
        self.name = name
        self.destination = destination
        self.burn = Destiny.Shield.get(burn)
        self.embed_url = embed_url
        self.legend = Destiny.Difficulty(**legend)
        self.master = Destiny.Difficulty(**master)

    @property
    def champion_types(self) -> set[Destiny.Champion]:
        return set(self.legend.champion_types + self.master.champion_types)

    @property
    def shield_types(self) -> set[Destiny.Shield]:
        return set(self.legend.shield_types + self.master.shield_types)

    @property
    def champion_list(self) -> str:
        return ", ".join(str(champion) for champion in self.champion_types)

    @property
    def shield_list(self) -> str:
        return ", ".join(str(shield) for shield in self.shield_types)

    @classmethod
    def get(cls, search: str):
        for lost_sector in cls.lost_sectors:
            if lost_sector.name == search:
                return lost_sector
        else:
            raise Destiny.Errors.LostSectorNotFoundError(search)

    @classmethod
    def get_current(cls):
        return cls.rotation[Destiny.get_day_index() // len(cls.rotation)]


with open("data/static/destiny/lost_sectors/lost_sectors.json", "r") as infile:
    lostSectorData: list[_LostSectorData] = json.load(infile)

LostSector.lost_sectors = [LostSector(**data) for data in lostSectorData]


with open("data/static/destiny/lost_sectors/rotation.json") as infile:
    rotation_data = json.load(infile)

for sector_name in rotation_data:
    if sector_name is None:
        LostSector.rotation.append(None)
    else:
        LostSector.rotation.append(LostSector.get(sector_name))
