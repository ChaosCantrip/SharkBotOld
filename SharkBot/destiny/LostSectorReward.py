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
        name="Exotic Helm",
        icon="(Helm Icon)"
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
