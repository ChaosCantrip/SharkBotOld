import json
import os
from datetime import datetime, timedelta
from typing import Union

from SharkBot import Cooldown, MemberInventory, MemberCollection, Mission, MemberStats, Utils, XP
from SharkBot.Handlers import firestoreHandler

birthdayFormat = "%d/%m/%Y"
membersDirectory = "data/live/members"


class Member:

    def __init__(self, member_data: dict) -> None:

        for item, value in defaultValues.items():
            if item not in member_data:
                member_data[item] = value

        self.id: int = member_data["id"]
        self.balance: int = member_data["balance"]
        self.inventory = MemberInventory(self, member_data["inventory"])
        self.collection = MemberCollection(self, member_data["collection"])
        self.counts: int = member_data["counts"]
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
        self.lastClaimedBirthday: int = member_data["lastClaimedBirthday"]
        self.stats = MemberStats(member_data["stats"])
        self.last_claimed_advent: int = member_data["last_claimed_advent"]
        self.xp = XP(member_data["xp"], self)
        self.legacy: dict = member_data["legacy"]
        self.used_codes: list[str] = member_data["used_codes"]
        self._discord_user = None

    async def fetch_discord_user(self, bot):
        if self._discord_user is None:
            discord_user = bot.get_user(self.id)
            if discord_user is None:
                discord_user = await bot.fetch_user(self.id)
            self._discord_user = discord_user
        return self._discord_user

    @property
    def snapshot_data(self) -> dict[str, Union[str, int]]:
        display_name = f"{self._discord_user.name}#{self._discord_user.discriminator}"
        avatar_url = f"https://cdn.discordapp.com/avatars/{self.id}/{self._discord_user.display_avatar.key}.jpg?size=256"
        return {
            "display_name": display_name,
            "avatar_url": avatar_url,
            "counts": self.counts,
            "xp": self.xp.xp,
            "level": self.xp.level
        }

    def write_data(self, upload: bool = False) -> None:
        """
        Saves the Member data to the .json

        :param upload: Whether to upload the data to Firestore or not
        """

        member_data = {
            "id": self.id,
            "balance": self.balance,
            "inventory": self.inventory.item_ids,
            "collection": self.collection.item_ids,
            "counts": self.counts,
            "cooldowns": {
                "hourly": self.cooldowns["hourly"].timestring,
                "daily": self.cooldowns["daily"].timestring,
                "weekly": self.cooldowns["weekly"].timestring
            },
            "missions": self.missions.data,
            "birthday": None if self.birthday is None else datetime.strftime(self.birthday, birthdayFormat),
            "lastClaimedBirthday": self.lastClaimedBirthday,
            "stats": self.stats.data,
            "last_claimed_advent": self.last_claimed_advent,
            "xp": self.xp.xp,
            "legacy": self.legacy,
            "used_codes": self.used_codes
        }

        with open(f"{membersDirectory}/{self.id}.json", "w") as outfile:
            json.dump(member_data, outfile, indent=4)

        if upload:
            self.upload_data()

    def upload_data(self) -> None:
        """
        Uploads the Member data to Firestore
        """

        firestoreHandler.upload_member(
            {
                "id": self.id,
                "balance": self.balance,
                "inventory": self.inventory.item_ids,
                "collection": self.collection.item_ids,
                "counts": self.counts
            }
        )

    # Cleanup

    def delete_file(self) -> None:
        """
        Deletes the Member's .json data file
        """

        os.remove(f"{membersDirectory}/{self.id}.json")
        global members
        del members[self.id]


def get(member_id: int) -> Member:
    if member_id not in members:
        member = Member(defaultValues)
        member.id = member_id
        member.write_data()

        with open(f"{membersDirectory}/{member.id}.json", "r") as infile:
            data = json.load(infile)
        member = Member(data)
        members[member_id] = member

    member = members[member_id]
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
    "stats": {},
    "last_claimed_advent": 0,
    "xp": 0,
    "legacy": {},
    "used_codes": []
}


def load_member_files() -> None:
    global members
    members = {}
    for filename in Utils.get_dir_filepaths(membersDirectory, ".json"):
        with open(filename, "r") as infile:
            data = json.load(infile)
            member = Member(data)
            members[int(data["id"])] = member


if not os.path.exists(membersDirectory):  # Ensure members folder exists
    os.makedirs(membersDirectory)

members = {}
load_member_files()
