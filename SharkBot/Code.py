import json
import os
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
            json.dump(list([code.data for code in cls.codes]), outfile, indent=4)

    @classmethod
    def load_codes(cls):
        cls.codes = []
        with open(_data_path, "r") as infile:
            data: list[_CodeData] = json.load(infile)
        for code_data in data:
            cls.codes.append(
                cls(**code_data)
            )

    def add_reward(self, reward_type: str, reward: str | int):
        if reward_type == "money":
            for r in self.rewards:
                if r["reward_type"] == "money":
                    r["reward"] += reward
                    return

        self.rewards.append(
            {
                "reward_type": reward_type,
                "reward": reward
            }
        )

    @classmethod
    def add_code(cls, code: str):
        code = code.upper()
        for c in cls.codes:
            if c.code == code:
                raise SharkBot.Errors.CodeAlreadyExistsError(code)
        else:
            cls.codes.append(
                cls(
                    code=code,
                    rewards=[]
                )
            )
        cls.write_codes()


if not os.path.exists(_data_path):
    with open(_data_path, "w+") as outfile:
        json.dump([], outfile, indent=4)


Code.load_codes()
