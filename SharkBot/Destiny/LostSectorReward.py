import json
from . import Errors as DestinyErrors
from SharkBot import Destiny


class LostSectorReward:
    rewards = []
    rotation = []

    def __init__(self, name: str, icon: str) -> None:
        self.name = name
        self.icon = icon

    def __str__(self) -> str:
        return f"{self.icon} {self.name}"

    @classmethod
    def get(cls, search: str):
        for reward in cls.rewards:
            if reward.name == search:
                return reward
        else:
            raise DestinyErrors.LostSectorRewardNotFoundError(search)

    @classmethod
    def get_current(cls):
        return cls.rotation[Destiny.get_day_index() % len(cls.rotation)]


LostSectorReward.rewards = [
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


with open("data/static/destiny/lost_sectors/loot_rotation.json") as infile:
    LostSectorReward.rotation = [LostSectorReward.get(reward) for reward in json.load(infile)]
