import json
import os
from datetime import datetime, timedelta
from typing import Union, Optional
import discord

from SharkBot import Cooldown, MemberInventory, MemberCollection, MemberVault, Mission, MemberStats, Utils, XP, Errors, Discord, IDs, Handlers

BIRTHDAY_FORMAT = "%d/%m/%Y"
_MEMBERS_DIRECTORY = "data/live/members"
_SNAPSHOTS_DIRECTORY = "data/live/snapshots/members"
REQUIRED_PATHS = [
    _MEMBERS_DIRECTORY, _SNAPSHOTS_DIRECTORY
]
UPDATED_JSON = "data/live/snapshots/members/updates.json"


class Member:

    def __init__(self, member_data: dict) -> None:

        for item, value in defaultValues.items():
            if item not in member_data:
                member_data[item] = value

        self.id: int = member_data["id"]
        self.balance: int = member_data["balance"]
        self._bank_balance: int = member_data["bank_balance"]
        self.inventory = MemberInventory(self, member_data["inventory"])
        self.collection = MemberCollection(self, member_data["collection"])
        self.vault = MemberVault(**member_data["vault"])
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
            self.birthday = datetime.strptime(member_data["birthday"], BIRTHDAY_FORMAT)
        self.lastClaimedBirthday: int = member_data["lastClaimedBirthday"]
        self.stats = MemberStats(member_data["stats"])
        self.last_claimed_advent: int = member_data["last_claimed_advent"]
        self.xp = XP(member_data["xp"], self)
        self.legacy: dict = member_data["legacy"]
        self.used_codes: list[str] = member_data["used_codes"]
        self._discord_user: Optional[discord.User] = None
        self._discord_member: Optional[discord.Member] = None

    async def fetch_discord_user(self):
        if self._discord_user is None:
            self._discord_user = Discord.bot.get_user(self.id)
            if self._discord_user is None:
                self._discord_user = await Discord.bot.fetch_user(self.id)

    async def fetch_discord_member(self):
        if self._discord_member is None:
            server = Discord.bot.get_guild(IDs.servers["Shark Exorcist"])
            if server is None:
                server = await Discord.bot.fetch_guild(IDs.servers["Shark Exorcist"])
            self._discord_member = server.get_member(self.id)
            if self._discord_member is None:
                self._discord_user = await server.fetch_member(self.id)

    @property
    def discord_user(self) -> discord.User:
        if self._discord_user is None:
            self._discord_user = Discord.bot.get_user(self.id)
        return self._discord_user

    @property
    def discord_member(self) -> discord.Member:
        if self._discord_member is None:
            server = Discord.bot.get_guild(IDs.servers["Shark Exorcist"])
            self._discord_member = server.get_member(self.id)
        return self._discord_member

    @property
    def snapshot_data(self) -> Optional[dict[str, Union[str, int]]]:
        if self.discord_member is None:
            return None
        return {
            "id": str(self.id),
            "display_name": self.discord_member.display_name,
            "avatar_url": self.discord_member.display_avatar.replace(size=256).url,
            "balance": self.balance,
            "bank_balance": self._bank_balance,
            "counts": self.counts,
            "xp": self.xp.xp,
            "level": self.xp.level
        }

    @property
    def wiki_profile_url(self) -> str:
        return f"https://sharkbot.online/profile/{self.id}"

    def write_data(self, upload: bool = True) -> None:
        """
        Saves the Member data to the .json

        :param upload: Whether to upload the data to Firestore
        """

        member_data = {
            "id": self.id,
            "balance": self.balance,
            "bank_balance": self._bank_balance,
            "inventory": self.inventory.item_ids,
            "collection": self.collection.item_ids,
            "vault": self.vault.data,
            "counts": self.counts,
            "cooldowns": {
                "hourly": self.cooldowns["hourly"].timestring,
                "daily": self.cooldowns["daily"].timestring,
                "weekly": self.cooldowns["weekly"].timestring
            },
            "missions": self.missions.data,
            "birthday": None if self.birthday is None else datetime.strftime(self.birthday, BIRTHDAY_FORMAT),
            "lastClaimedBirthday": self.lastClaimedBirthday,
            "stats": self.stats.data,
            "last_claimed_advent": self.last_claimed_advent,
            "xp": self.xp.xp,
            "legacy": self.legacy,
            "used_codes": self.used_codes
        }

        with open(f"{_MEMBERS_DIRECTORY}/{self.id}.json", "w") as outfile:
            json.dump(member_data, outfile, indent=4)

        if upload:
            self.upload_data()

    @property
    def snapshot_has_changed(self) -> bool:
        if not os.path.exists(f"{_SNAPSHOTS_DIRECTORY}/{self.id}.json"):
            return True
        with open(f"{_SNAPSHOTS_DIRECTORY}/{self.id}.json", "r") as infile:
            old_snapshot = json.load(infile)

        return old_snapshot != self.snapshot_data

    def write_snapshot(self, snapshot: Optional[dict]):
        if snapshot is None:
            snapshot = self.snapshot_data
        with open(f"{_SNAPSHOTS_DIRECTORY}/{self.id}.json", "w+") as outfile:
            json.dump(snapshot, outfile, indent=2)

    def upload_data(self, force_upload: bool = False) -> None:
        if force_upload or self.snapshot_has_changed:
            snapshot = self.snapshot_data
            if snapshot is None:
                return
            Handlers.firestoreHandler.upload_data(snapshot)
            self.write_snapshot(snapshot)
            with open(UPDATED_JSON, "r+") as updated_file:
                updated_list: dict[str, str] = json.load(updated_file)
                if str(self.id) not in updated_list:
                    updated_list[str(self.id)] = self.discord_user.display_name
                    json.dump(updated_list, updated_file, indent=2)

    # Banking

    @property
    def bank_balance(self) -> int:
        return self._bank_balance

    @bank_balance.setter
    def bank_balance(self, value: int):
        if value < 0:
            raise Errors.BankBalanceBelowZeroError(self.id, value)
        else:
            self._bank_balance = value

    # Cleanup

    def delete_file(self) -> None:
        """
        Deletes the Member's .json data file
        """

        os.remove(f"{_MEMBERS_DIRECTORY}/{self.id}.json")
        global members
        del members[self.id]


def get(member_id: int) -> Member:
    if member_id not in members:
        member = Member(defaultValues)
        member.id = member_id
        member.write_data()

        with open(f"{_MEMBERS_DIRECTORY}/{member.id}.json", "r") as infile:
            data = json.load(infile)
        member = Member(data)
        members[member_id] = member

    member = members[member_id]
    return member


defaultValues = {
    "id": 0,
    "balance": 0,
    "bank_balance": 0,
    "inventory": [],
    "collection": [],
    "vault": {
        "items": [],
        "auto": []
    },
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
    for filename in Utils.get_dir_filepaths(_MEMBERS_DIRECTORY, ".json"):
        with open(filename, "r") as infile:
            data = json.load(infile)
            member = Member(data)
            members[int(data["id"])] = member


for path in REQUIRED_PATHS:
    Utils.FileChecker.directory(path)
Utils.FileChecker.json(UPDATED_JSON, [])

members: dict[int, Member] = {}
load_member_files()
