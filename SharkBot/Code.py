import json
from typing import TypedDict

import SharkBot

_data_path = "data/live/bot/codes.json"


class _RewardData(TypedDict):
    reward_type: str
    reward: int | str


class _CodeData(TypedDict):
    code: str
    rewards: list[_RewardData]


class Code:
    codes = []

    def __init__(self, code: str, rewards: list[_RewardData]):
        self.code = code
        self.rewards = rewards

    @classmethod
    def get(cls, search: str):
        search = search.upper()
        for code in cls.codes:
            if code.code == search:
                return code
        else:
            raise SharkBot.Errors.InvalidCodeError(search)

    @property
    def data(self) -> _CodeData:
        return {
            "code": self.code,
            "rewards": self.rewards
        }

    @classmethod
    def write_codes(cls):
        with open(_data_path, "w+") as outfile:
            json.dump(list([code.data for code in cls.codes]), outfile)
