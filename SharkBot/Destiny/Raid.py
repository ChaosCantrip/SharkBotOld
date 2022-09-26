import json
from typing import TypedDict
from datetime import date, datetime, timedelta

from SharkBot import Destiny


class _RaidData(TypedDict):
    name: str


class _RotationData(TypedDict):
    seasonal: str
    featured: list[str]


class Raid:

    def __init__(self, name: str) -> None:
        self.name = name


with open("data/static/destiny/raids/raids.json", "r") as infile:
    raidData: list[_RaidData] = json.load(infile)

raids: list[Raid] = [Raid(**data) for data in raidData]


def get(search: str) -> Raid:
    for raid in raids:
        if raid.name == search:
            return raid
    else:
        raise Destiny.Errors.RaidNotFoundError(search)


with open("data/static/destiny/raids/rotation.json", "r") as infile:
    rotationData: _RotationData = json.load(infile)

seasonal: Raid = get(rotationData["seasonal"])
rotation: list[Raid] = [get(raidName) for raidName in rotationData["featured"]]
rotationStart = date(year=2022, month=8, day=23)


def get_current() -> Raid:
    dtnow = datetime.utcnow()
    if dtnow.time() < Destiny.resetTime:
        dtnow = dtnow - timedelta(days=1)
    days = (dtnow - rotationStart).days
    weeks = int(days / 7)
    position = weeks % len(rotation)
    return rotation[position]
