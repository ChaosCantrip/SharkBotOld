import json
from typing import Union
from SharkBot.destiny import Champion, Shield, Errors as DestinyErrors


class LostSector:

    def __init__(self, data: dict[str, Union[str, dict[str, list[str]]]]):
        self.name: str = data["name"]
        self.champions: list[Champion.Champion] = [Champion.get(champion) for champion in data["legend"]["champions"]]
        self.shields: list[Shield.Shield] = [Shield.get(shield) for shield in data["legend"]["shields"]]

    @property
    def champion_list(self) -> str:
        return ", ".join(champion.text for champion in self.champions)


with open("staticdata/destiny/lost_sectors/lost_sectors.json", "r") as infile:
    lostSectorData = json.load(infile)

lostSectors = [LostSector(data) for data in lostSectorData]


def get(search: str) -> LostSector:
    for lostSector in lostSectors:
        if lostSector.name == search:
            return lostSector
    else:
        raise DestinyErrors.LostSectorNotFoundError(search)
