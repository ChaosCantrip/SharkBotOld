import json
import os

import SharkBot

api_folder_path = "data/live/api"

if not os.path.exists(api_folder_path):  # Ensure api folder exists
    os.makedirs(api_folder_path)

if not os.path.exists(f"{api_folder_path}/last_counts.json"):
    with open(f"{api_folder_path}/last_counts.json", "w+") as outfile:
        json.dump({}, outfile, indent=4)


def check_changed_counts() -> list[SharkBot.Member.Member]:
    output = []
    with open(f"{api_folder_path}/last_counts.json", "r") as infile:
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
    with open(f"{api_folder_path}/last_counts.json", "w+") as outfile:
        json.dump(data, outfile, indent=4)
