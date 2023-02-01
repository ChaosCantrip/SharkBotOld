import json
import os.path
from typing import Callable, Union, Optional, Self

from discord.ext import commands

import SharkBot

_LEADERBOARD_FORMAT = dict[str, Union[int, float]]

_SNAPSHOTS_DICT = "data/live/snapshots/leaderboards"
SharkBot.Utils.FileChecker.directory(_SNAPSHOTS_DICT)

class _LeaderboardMember:

    def __init__(self, rank: int, member: SharkBot.Member.Member, value: Union[int, float], leaderboard):
        self.rank = rank
        self.member = member
        self.value = value
        self.leaderboard: Leaderboard = leaderboard

    def __lt__(self, other: Self):
        return self.value < other.value

    def __repr__(self) -> str:
        return "LeaderboardMember[\n" + "\n  ".join(json.dumps(self.repr_data, indent=2).split("\n")) + "\n]"

    def __str__(self) -> str:
        return f"{self.rank}. {self.member.display_name} - {self.print_value}"

    @property
    def print_value(self) -> str:
        return self.leaderboard.print_format(str(self.value))

    @property
    def repr_data(self) -> dict:
        return {
            "Rank": self.rank,
            "Value": self.value,
            "Member": {
                "id": self.member.id,
                "name": self.member.display_name
            }
        }

    @property
    def member_id_str(self) -> str:
        return str(self.member.id)

    @property
    def data(self) -> dict[str, Union[str, int, float]]:
        return {
            "rank": self.rank,
            "value": self.value,
            "print_value": self.print_value,
            "member": {
                "id": str(self.member.id),
                "name": self.member.display_name
            }
        }

class Leaderboard:
    _leaderboards_dict: dict[str, Self] = {}
    leaderboards: list[Self] = []

    def __init__(self, name: str, method: Callable[[SharkBot.Member.Member], Union[int, float]], print_format: Callable[[str], str] = lambda s: s, high_to_low: bool = True):
        self.name = name
        self.method = method
        self.doc_name = "_".join(self.name.lower().split(" "))
        self.save_file = f"{_SNAPSHOTS_DICT}/{self.doc_name}.json"
        self.high_to_low = high_to_low
        self.last_snapshot: Optional[_LEADERBOARD_FORMAT] = None
        self.print_format = print_format
        if os.path.isfile(self.save_file):
            with open(self.save_file, "r") as _infile:
                self.last_snapshot = json.load(_infile)

    def __repr__(self) -> str:
        _data = {
            "Name": self.name,
            "Doc Name": self.doc_name,
            "Save File": self.save_file,
            "High to Low": self.high_to_low,
            "Ranked Snapshot": [lb_member.repr_data for lb_member in self.create_ranked()]
        }
        return "Leaderboard" + json.dumps(_data, indent=2)

    @classmethod
    async def convert(cls, ctx: commands.Context, argument: str):
        return cls.get(argument)

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

    def create_ranked(self, snapshot: Optional[_LEADERBOARD_FORMAT] = None) -> list[_LeaderboardMember]:
        if snapshot is None:
            snapshot = self.create_current()
            lb_dict = {SharkBot.Member.get(int(member_id)): value for member_id, value in snapshot.items()}
        else:
            lb_dict = {member: self.method(member) for member in SharkBot.Member.members}
        lb_list = [_LeaderboardMember(-1, member, value, self) for member, value in lb_dict.items()]
        lb_list.sort(reverse=self.high_to_low)
        rank = 1
        last_value = lb_list[0].value
        for true_rank, lb_member in enumerate(lb_list):
            if lb_member.value != last_value:
                rank = true_rank + 1
                last_value = lb_member.value
            lb_member.rank = rank
        return lb_list

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
            return snapshot != self.last_snapshot

    def upload(self, ranked_snapshot: Optional[list[_LeaderboardMember]] = None):
        if ranked_snapshot is None:
            ranked_snapshot = self.create_ranked()
        _data = {
            "id": self.doc_name,
            "name": self.name,
            "rankings": [
                lb_member.data for lb_member in ranked_snapshot if lb_member.value > 0
            ]
        }
        SharkBot.Handlers.firestoreHandler.set_doc("leaderboards", self.doc_name, _data)

Leaderboard.leaderboards = [
    Leaderboard(name="Counts", method=lambda m: m.counts),
    Leaderboard(name="Incorrect Counts", method=lambda m: m.stats.incorrect_counts),
    Leaderboard(name="Coinflips", method=lambda m: m.stats.coinflips.num),
    Leaderboard(name="Coinflips Won", method=lambda m: m.stats.coinflips.wins),
    Leaderboard(name="Coinflips Lost", method=lambda m: m.stats.coinflips.losses),
    Leaderboard(name="Coinflip Mercies", method=lambda m: m.stats.coinflips.mercies),
    Leaderboard(name="Coinflip Winrate", method=lambda m: m.stats.coinflips.winrate, print_format=lambda s: f"{s}%"),
    Leaderboard(name="Boxes Claimed", method=lambda m: m.stats.boxes.claimed),
    Leaderboard(name="Boxes Bought", method=lambda m: m.stats.boxes.bought),
    Leaderboard(name="Counting Boxes", method=lambda m: m.stats.boxes.counting),
    Leaderboard(name="Items Sold", method=lambda m: m.stats.sold_items),
    Leaderboard(name="Balance", method=lambda m: m.balance),
    Leaderboard(name="XP", method=lambda m: m.xp.xp),
    Leaderboard(name="Level", method=lambda m: m.xp.level),
    Leaderboard(name="Collections", method=lambda m: len(m.collection), print_format=lambda s: f"{s} Items"),
    Leaderboard(name="Missions Completed", method=lambda m: m.stats.completed_missions)
]
Leaderboard.build_dict()