import json
import os
from typing import TypedDict, Union

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

    @classmethod
    def a_get(cls, search: str):
        try:
            return cls.get(search)
        except SharkBot.Errors.InvalidCodeError:
            raise SharkBot.Errors.CodeDoesNotExistError(search)

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
                    self.write_codes()
                    return

        if reward_type == "xp":
            for r in self.rewards:
                if r["reward_type"] == "xp":
                    r["reward"] += reward
                    self.write_codes()
                    return

        self.rewards.append(
            {
                "reward_type": reward_type,
                "reward": reward
            }
        )
        self.write_codes()

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

    @classmethod
    def remove_code(cls, search: str):
        code = cls.a_get(search)
        cls.codes.remove(code)
        cls.write_codes()

    @property
    def expired(self) -> bool:
        return False

    @property
    def money_reward(self) -> Union[None, int]:
        for reward in self.rewards:
            if reward["reward_type"] == "money":
                return reward["reward"]
        else:
            return None

    @property
    def item_rewards(self) -> Union[None, list[SharkBot.Item.Item]]:
        output = []
        for reward in self.rewards:
            if reward["reward_type"] == "item":
                output.append(SharkBot.Item.get(reward["reward"]))
        return output if len(output) > 0 else None

    @property
    def xp_reward(self) -> Union[None, int]:
        for reward in self.rewards:
            if reward["reward_type"] == "xp":
                return reward["reward"]
        else:
            return None


if not os.path.exists(_data_path):
    with open(_data_path, "w+") as outfile:
        json.dump([], outfile, indent=4)


Code.load_codes()
