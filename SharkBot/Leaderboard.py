import json
import os.path
from typing import Callable, Union, Optional, Self

import SharkBot

_LEADERBOARD_FORMAT = dict[str, Union[int, float]]

_SNAPSHOTS_DICT = "data/live/snapshots/leaderboards"
SharkBot.Utils.FileChecker.directory(_SNAPSHOTS_DICT)

class _LeaderboardMember:

    def __init__(self, rank: int, member: SharkBot.Member.Member, value: Union[int, float]):
        self.rank = rank
        self.member = member
        self.value = value

    def __lt__(self, other: Self):
        return self.value < other.value

    @property
    def member_id_str(self) -> str:
        return str(self.member.id)

class Leaderboard:
    _leaderboards_dict: dict[str, Self] = {}
    leaderboards: list[Self] = []

    def __init__(self, name: str, method: Callable[[SharkBot.Member.Member], Union[int, float]]):
        self.name = name
        self.method = method
        self.doc_name = "_".join(self.name.lower().split(" "))
        self.save_file = _SNAPSHOTS_DICT + self.doc_name + ".json"
        self.last_snapshot: Optional[_LEADERBOARD_FORMAT] = None
        if os.path.isfile(self.save_file):
            with open(self.save_file, "r") as _infile:
                self.last_snapshot = json.load(_infile)

    @classmethod
    def get(cls, search: str) -> Self:
        try:
            return cls._leaderboards_dict[search.lower()]
        except KeyError:
            raise SharkBot.Errors.LeaderboardNotFoundError(search)

    @classmethod
    def build_dict(cls) -> None:
        cls._leaderboards_dict = {lb.name.lower(): lb for lb in cls.leaderboards}

    def create_current(self) -> _LEADERBOARD_FORMAT:
        return {str(member.id): self.method(member) for member in SharkBot.Member.members}

    def save_snapshot(self, snapshot: Optional[_LEADERBOARD_FORMAT] = None) -> None:
        if snapshot is None:
            snapshot = self.create_current()
        self.last_snapshot = snapshot
        with open(self.save_file, "w+") as _outfile:
            json.dump(snapshot, _outfile, indent=2)

    def has_changed(self, snapshot: Optional[_LEADERBOARD_FORMAT] = None) -> bool:
        if snapshot is None:
            snapshot = self.create_current()
        if self.last_snapshot is None:
            return True
        else:
            return snapshot == self.last_snapshot
