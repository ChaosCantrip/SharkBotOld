import json
import SharkBot


def check_changed_counts() -> list[SharkBot.Member.Member]:
    output = []
    with open("data/live/api/last_counts.json", "r") as infile:
        data: dict[int, int] = json.load(infile)
    for member in SharkBot.Member.members.values():
        if member.id not in data.keys():
            output.append(member)
        else:
            if member.counts != data[member.id]:
                output.append(member)
    return output


def write_counts():
    data = {member.id: member.counts for member in SharkBot.Member.members.values()}
    with open("data/live/api/last_counts.json", "w+") as outfile:
        json.dump(data, outfile, indent=4)
