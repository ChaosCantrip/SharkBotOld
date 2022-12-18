import json
import os

import SharkBot

api_folder_path = "data/live/api"

if not os.path.exists(api_folder_path):  # Ensure api folder exists
    os.makedirs(api_folder_path)

if not os.path.exists(f"{api_folder_path}/last_upload.json"):
    with open(f"{api_folder_path}/last_upload.json", "w+") as outfile:
        json.dump({}, outfile, indent=4)


def check_differences() -> dict[str, dict[str, int]]:
    output = {}
    with open(f"{api_folder_path}/last_upload.json", "r") as infile:
        data: dict[str, dict[str, int]] = json.load(infile)
    for member in SharkBot.Member.members.values():
        member_data = member.snapshot_data
        member_id = str(member.id)
        if member_id not in data.keys():
            output[member.id] = member_data
        else:
            saved_data = data[member_id]
            if member_data != saved_data:
                output[member_id] = {}
                for key, value in member_data.items():
                    if key not in saved_data.keys() or saved_data[key] != value:
                        output[str(member.id)][key] = value
    return output


def write_snapshot():
    data = {member.id: member.snapshot_data for member in SharkBot.Member.members.values()}
    with open(f"{api_folder_path}/last_upload.json", "w+") as outfile:
        json.dump(data, outfile, indent=4)
