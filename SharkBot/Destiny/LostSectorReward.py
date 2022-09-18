import datetime
import json
from . import Errors as DestinyErrors


class LostSectorReward:

    def __init__(self, name: str, icon: str) -> None:
        self.name = name
        self.icon = icon

    @property
    def text(self) -> str:
        return f"{self.icon} {self.name}"


rewards = [
    LostSectorReward(
        name="Exotic Head",
        icon="<:head_icon:1020115308821880852>"
    ),
    LostSectorReward(
        name="Exotic Arms",
        icon="<:arms_icon:1020115271031205948>"
    ),
    LostSectorReward(
        name="Exotic Chest",
        icon="<:chest_icon:1020115283421188127>"
    ),
    LostSectorReward(
        name="Exotic Legs",
        icon="<:legs_icon:1020115295446257694>"
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