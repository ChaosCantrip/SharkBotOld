from SharkBot import Destiny
from typing import TypedDict


class _DifficultyData(TypedDict):
    champions: dict[str, int]
    shields: dict[str, int]


class Nightfall:

    def __init__(self, name: str, destination: str, legend: _DifficultyData, master: _DifficultyData):
        self.name = name
        self.destination = destination
        self.legend = Destiny.LostSector.Difficulty(**legend)
        self.master = Destiny.LostSector.Difficulty(**master)