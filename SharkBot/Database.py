import json
import os
from typing import Union

import SharkBot

db_folder_path = "data/live/db"

if not os.path.exists(db_folder_path):  # Ensure db folder exists
    os.makedirs(db_folder_path)

if not os.path.exists(f"{db_folder_path}/last_upload.json"):
    with open(f"{db_folder_path}/last_upload.json", "w+") as outfile:
        json.dump({}, outfile, indent=4)


def check_differences() -> list[dict]:
    output = []
    with open(f"{db_folder_path}/last_upload.json", "r") as infile:
        data: dict[str, dict[str, int]] = json.load(infile)
    for member in SharkBot.Member.members.values():
        member_data = member.snapshot_data
        if str(member.id) not in data.keys() or data[str(member.id)] != member_data:
            output.append(member_data)
    return output


def write_snapshot() -> None:
    data = {member.id: member.snapshot_data for member in SharkBot.Member.members.values()}
    with open(f"{db_folder_path}/last_upload.json", "w+") as outfile:
        json.dump(data, outfile, indent=4)
