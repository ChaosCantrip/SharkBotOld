from typing import TypedDict


class _RewardData(TypedDict):
    reward_type: str
    reward: int | str


class _CodeData(TypedDict):
    code: str
    rewards: list[_RewardData]


class Code:

    def __init__(self, code: str, rewards: list[_RewardData]):
        self.code = code
        self.rewards = rewards
