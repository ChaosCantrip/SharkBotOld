import json
from typing import TypedDict
from datetime import date, datetime, timedelta

from SharkBot import Destiny


class _DungeonData(TypedDict):
    name: str
    destination: str


class _RotationData(TypedDict):
    seasonal: str
    featured: list[str]


class Dungeon:

    def __init__(self, name: str, destination: str) -> None:
        self.name = name
        self.destination = destination


with open("data/static/destiny/dungeons/dungeons.json", "r") as infile:
    dungeonData: list[_DungeonData] = json.load(infile)

dungeons: list[Dungeon] = [Dungeon(**data) for data in dungeonData]


def get(search: str) -> Dungeon:
    for dungeon in dungeons:
        if dungeon.name == search:
            return dungeon
    else:
        raise Destiny.Errors.DungeonNotFoundError(search)


with open("data/static/destiny/dungeons/rotation.json", "r") as infile:
    rotationData: _RotationData = json.load(infile)

seasonal: Dungeon = get(rotationData["seasonal"])
rotation: list[Dungeon] = [get(dungeonName) for dungeonName in rotationData["featured"]]
rotationStart = date(year=2022, month=8, day=23)


def get_current() -> Dungeon:
    dtnow = datetime.utcnow()
    if dtnow.time() < Destiny.resetTime:
        dtnow = dtnow - timedelta(days=1)
    days = (dtnow - rotationStart).days
    weeks = int(days / 7)
    position = weeks % len(rotation)
    return rotation[position]
