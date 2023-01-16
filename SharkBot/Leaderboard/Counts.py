import json
from typing import Union

from SharkBot import Member, Utils

_FILEPATH = "data/live/leaderboards/counts.json"
Utils.FileChecker.json(_FILEPATH, [])

class Counts:

    @staticmethod
    def get_current() -> list[dict[str, Union[Member.Member, int]]]:
        members = [member for member in Member.members if member.counts > 0]
        members.sort(key=lambda m: m.counts, reverse=True)

        table = []
        last_counts = 25000
        rank = 0
        true_rank = 0
        for member in members:
            true_rank += 1
            if member.counts < last_counts:
                last_counts = member.counts
                rank = true_rank

            table.append({
                "member": member,
                "rank": rank,
                "counts": member.counts
            })

        return table

    @staticmethod
    def get_saved() -> list[dict[str, Union[Member.Member, int]]]:
        with open(_FILEPATH, "r") as infile:
            data: list[dict[str, Union[Member.Member, int]]] = json.load(infile)
        for member_data in data:
            member_data["member"] = Member.get(member_data["member"])
        return data

    @classmethod
    def has_changed(cls) -> bool:
        return cls.get_saved() == cls.get_current()

