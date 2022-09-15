import json
from typing import Union
from SharkBot.destiny import Champion, Shield


class LostSector:

    def __init__(self, data: dict[str, Union[str, dict[str, list[str]]]]):
        self.name: str = data["name"]
        self.champions: list[Champion.Champion] = [Champion.get(champion) for champion in data["legend"]["champions"]]
        self.shields: list[Shield.Shield] = [Shield.get(shield) for shield in data["legend"]["shields"]]


with open("staticdata/destiny/lost_sectors/lost_sectors.json", "r") as infile:
    lostSectorData = json.load(infile)

lostSectors = [LostSector(data) for data in lostSectorData]
