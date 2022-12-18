import json
import os

import SharkBot

api_folder_path = "data/live/api"

if not os.path.exists(api_folder_path):  # Ensure api folder exists
    os.makedirs(api_folder_path)

if not os.path.exists(f"{api_folder_path}/last_upload.json"):
    with open(f"{api_folder_path}/last_upload.json", "w+") as outfile:
        json.dump({}, outfile, indent=4)


def check_differences() -> dict[int, dict[str, int]]:
    output = {}
    with open(f"{api_folder_path}/last_upload.json", "r") as infile:
        data: dict[int, dict[str, int]] = json.load(infile)
    for member in SharkBot.Member.members.values():
        member_data = member.snapshot_data
        if member.id not in data.keys():
            output[member.id] = member_data
        else:
            if member_data != data[member.id]:
                output[member.id] = {}
                for key in ["display_name", "avatar_url", "counts"]:
                    if member_data[key] != data[member.id][key]:
                        output[member.id][key] = member_data[key]
    return output


def write_snapshot():
    data = {member.id: member.snapshot_data for member in SharkBot.Member.members.values()}
    with open(f"{api_folder_path}/last_upload.json", "w+") as outfile:
        json.dump(data, outfile, indent=4)
