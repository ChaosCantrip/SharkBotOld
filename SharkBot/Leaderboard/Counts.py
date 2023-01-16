import json
from typing import Union, Optional

from SharkBot import Member, Utils

_FILEPATH = "data/live/leaderboards/counts.json"
Utils.FileChecker.json(_FILEPATH, [])

class Counts:

    @staticmethod
    def get_current(include_counts: bool = True) -> list[dict[str, Union[Member.Member, int]]]:
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

        if not include_counts:
            for member_data in table:
                del member_data["counts"]

        return table

    @staticmethod
    def get_saved(include_counts: bool = True) -> list[dict[str, Union[Member.Member, int]]]:
        with open(_FILEPATH, "r") as infile:
            data: list[dict[str, Union[Member.Member, int]]] = json.load(infile)
        for member_data in data:
            member_data["member"] = Member.get(member_data["member"])

        if not include_counts:
            for member_data in data:
                del member_data["counts"]

        return data

    @classmethod
    def has_changed(cls) -> bool:
        return cls.get_saved(include_counts=False) == cls.get_current(include_counts=False)

    @classmethod
    def write(cls, data: Optional[list[dict[str, Union[Member.Member, int]]]]):
        if data is None:
            data = cls.get_current()
        with open(_FILEPATH, "w+") as outfile:
            json.dump(data, outfile, indent=2)

