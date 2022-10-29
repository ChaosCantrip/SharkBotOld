import datetime
import json
from . import Errors as DestinyErrors


class LostSectorReward:

    def __init__(self, name: str, icon: str) -> None:
        self.name = name
        self.icon = icon

    def __str__(self) -> str:
        return f"{self.icon} {self.name}"


rewards = [
    LostSectorReward(
        name="Exotic Head",
        icon="<:head_icon:1021291209257386004>"
    ),
    LostSectorReward(
        name="Exotic Arms",
        icon="<:arms_icon:1021291174931210290>"
    ),
    LostSectorReward(
        name="Exotic Chest",
        icon="<:chest_icon:1021291186381651978>"
    ),
    LostSectorReward(
        name="Exotic Legs",
        icon="<:legs_icon:1021291197836296232>"
    )
]


def get(search: str) -> LostSectorReward:
    for reward in rewards:
        if reward.name == search:
            return reward
    else:
        raise DestinyErrors.LostSectorRewardNotFoundError(search)


with open("data/static/destiny/lost_sectors/loot_rotation.json") as infile:
    rotation = [get(reward) for reward in json.load(infile)]

rotationStart = datetime.datetime(2022, 9, 13)
resetTime = datetime.time(18)


def get_current() -> LostSectorReward:
    dtnow = datetime.datetime.now()
    if dtnow.time() < resetTime:
        dtnow = dtnow - datetime.timedelta(days=1)
    days = (dtnow - rotationStart).days
    position = days % len(rotation)
    return rotation[position]
