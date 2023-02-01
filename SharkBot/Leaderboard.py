import json
from typing import Callable, Union, Optional, Self

import SharkBot

_SNAPSHOTS_DICT = "data/live/snapshots/leaderboards"
SharkBot.Utils.FileChecker.directory(_SNAPSHOTS_DICT)

class Leaderboard:
    _leaderboards_dict: dict[str, Self] = {}

    def __init__(self, name: str, method: Callable[[SharkBot.Member.Member], Union[int, float]]):
        self.name = name
        self.method = method
        self.doc_name = "_".join(self.name.lower().split(" "))
        self.save_file = _SNAPSHOTS_DICT + self.doc_name + ".json"

    @classmethod
    def get(cls, search: str) -> Self:
        try:
            return cls._leaderboards_dict[search.lower()]
        except KeyError:
            raise SharkBot.Errors.LeaderboardNotFoundError(search)

    def create_current(self) -> dict[str, Union[int, float]]:
        return {str(member.id): self.method(member) for member in SharkBot.Member.members}

    def save_snapshot(self, snapshot: Optional[dict[str, Union[int, float]]] = None):
        if snapshot is None:
            snapshot = self.create_current()
        with open(self.save_file, "w+") as _outfile:
            json.dump(snapshot, _outfile, indent=2)
