from typing import Union
from SharkBot.destiny import Champion, Shield


class LostSector:

    def __init__(self, data: dict[str, Union[str, dict[str, list[str]]]]):
        self.name: str = data["name"]
        self.champions: list[Champion.Champion] = [Champion.get(champion) for champion in data["champions"]]
        self.shields: list[Shield.Shield] = [Shield.get(shield) for shield in data["shields"]]
