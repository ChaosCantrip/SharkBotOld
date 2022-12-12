from typing import TypedDict


class _RewardData(TypedDict):
    reward_type: str
    reward: int | str


class _CodeData(TypedDict):
    code: str
    rewards: list[_RewardData]


class Code:
    pass
