import json
from typing import TypedDict


class _DungeonData(TypedDict):
    name: str
    destination: str


class Dungeon:

    def __init__(self, name: str, destination: str) -> None:
        self.name = name
        self.destination = destination


with open("data/static/destiny/dungeons/dungeons.json", "r") as infile:
    dungeonData: list[_DungeonData] = json.load(infile)

dungeons: list[Dungeon] = [Dungeon(**data) for data in dungeonData]
