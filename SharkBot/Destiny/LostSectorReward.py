import json
from . import Errors as DestinyErrors
from SharkBot import Destiny, Icon


class LostSectorReward:
    rewards = []
    rotation = []

    def __init__(self, name: str, icon: str) -> None:
        self.name = name
        self._icon = icon

    @property
    def icon(self) -> str:
        return Icon.get(self._icon)

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
        icon="head_icon"
    ),
    LostSectorReward(
        name="Exotic Arms",
        icon="arms_icon"
    ),
    LostSectorReward(
        name="Exotic Chest",
        icon="chest_icon"
    ),
    LostSectorReward(
        name="Exotic Legs",
        icon="legs_icon"
    )
]


with open("data/static/destiny/lost_sectors/loot_rotation.json") as infile:
    LostSectorReward.rotation = [LostSectorReward.get(reward) for reward in json.load(infile)]
