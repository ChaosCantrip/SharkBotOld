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
        icon="(Head Icon)"
    ),
    LostSectorReward(
        name="Exotic Arms",
        icon="(Arms Icon)"
    ),
    LostSectorReward(
        name="Exotic Chest",
        icon="(Chest Icon)"
    ),
    LostSectorReward(
        name="Exotic Legs",
        icon="(Legs Icon)"
    )
]


def get(search: str) -> LostSectorReward:
    for reward in rewards:
        if reward.name == search:
            return reward
    else:
        raise DestinyErrors.LostSectorRewardNotFoundError(search)


with open("staticdata/destiny/lost_sectors/loot_rotation.json") as infile:
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