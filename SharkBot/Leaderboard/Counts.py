from typing import Union

from SharkBot import Member

class Counts:

    @staticmethod
    def current() -> list[dict[str, Union[Member.Member, int]]]:
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
