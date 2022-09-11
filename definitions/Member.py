import json
import os
from datetime import datetime, timedelta

from definitions import Cooldown, MemberInventory, MemberCollection, Mission, MemberStats
from handlers import firestoreHandler

birthdayFormat = "%d/%m/%Y"


class Member:

    def __init__(self, member_data: dict) -> None:

        for item, value in defaultValues.items():
            if item not in member_data:
                member_data[item] = value

        self.id = member_data["id"]
        self.balance = member_data["balance"]
        self.inventory = MemberInventory.MemberInventory(self, member_data["inventory"])
        self.collection = MemberCollection.MemberCollection(self, member_data["collection"])
        self.counts = member_data["counts"]
        self.cooldowns = {
            "hourly": Cooldown.Cooldown("hourly", member_data["cooldowns"]["hourly"], timedelta(hours=1)),
            "daily": Cooldown.Cooldown("daily", member_data["cooldowns"]["daily"], timedelta(days=1)),
            "weekly": Cooldown.Cooldown("weekly", member_data["cooldowns"]["weekly"], timedelta(weeks=1))
        }
        self.missions = Mission.MemberMissions(self, member_data["missions"])
        if member_data["birthday"] is None:
            self.birthday = None
        else:
            self.birthday = datetime.strptime(member_data["birthday"], birthdayFormat)
        self.lastClaimedBirthday = member_data["lastClaimedBirthday"]
        self.stats = MemberStats.MemberStats(member_data["stats"])

    def write_data(self, upload: bool = True) -> None:

        member_data = {
            "id": self.id,
            "balance": self.balance,
            "inventory": self.inventory.itemids,
            "collection": self.collection.itemids,
            "counts": self.counts,
            "cooldowns": {
                "hourly": self.cooldowns["hourly"].timestring,
                "daily": self.cooldowns["daily"].timestring,
                "weekly": self.cooldowns["weekly"].timestring
            },
            "missions": self.missions.data,
            "birthday": None if self.birthday is None else datetime.strftime(self.birthday, birthdayFormat),
            "lastClaimedBirthday": self.lastClaimedBirthday,
            "stats": self.stats.data
        }

        with open(f"data/members/{self.id}.json", "w") as outfile:
            json.dump(member_data, outfile, indent=4)

        if upload:
            self.upload_data()

    def upload_data(self) -> None:
        firestoreHandler.upload_member(
            {
                "id": self.id,
                "balance": self.balance,
                "inventory": self.inventory.itemids,
                "collection": self.collection.itemids,
                "counts": self.counts
            }
        )

    # Cleanup

    def delete_file(self) -> None:
        os.remove(f"data/members/{self.id}.json")
        global members
        del members[self.id]


def get(memberid: int) -> Member:
    memberid = int(memberid)
    if memberid not in members:
        member = Member(defaultValues)
        member.id = memberid
        members[memberid] = member
        member.write_data()

    member = members[memberid]
    return member


defaultValues = {
    "id": 0,
    "balance": 0,
    "inventory": [],
    "collection": [],
    "counts": 0,
    "cooldowns": {
        "hourly": "01/01/2020-00:00:00",
        "daily": "01/01/2020-00:00:00",
        "weekly": "01/01/2020-00:00:00"
    },
    "missions": [],
    "birthday": None,
    "lastClaimedBirthday": 2021,
    "stats": {}
}


def load_member_files() -> None:
    global members
    members = {}
    for filename in os.listdir("./data/members"):
        with open(f"data/members/{filename}", "r") as infile:
            data = json.load(infile)
            member = Member(data)
            members[int(data["id"])] = member


members = {}
load_member_files()
