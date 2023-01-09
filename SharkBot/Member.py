import json
import os
from datetime import datetime, timedelta
from typing import Union, Optional
import discord
from discord.ext import commands

from SharkBot import MemberCooldowns, MemberInventory, MemberCollection, MemberVault, Mission, MemberStats, Utils, XP, Errors, IDs, Handlers, MemberDataConverter, MemberSnapshot

BIRTHDAY_FORMAT = "%d/%m/%Y"
_MEMBERS_DIRECTORY = "data/live/members"
_SNAPSHOTS_DIRECTORY = "data/live/snapshots/members"
REQUIRED_PATHS = [
    _MEMBERS_DIRECTORY, _SNAPSHOTS_DIRECTORY
]


class Member:

    def __init__(self, member_data: dict) -> None:

        member_data = MemberDataConverter.convert(member_data)

        self.id: int = member_data["id"]
        self.balance: int = member_data["balance"]
        self._bank_balance: int = member_data["bank_balance"]
        self.inventory = MemberInventory(self, member_data["inventory"])
        self.collection = MemberCollection(self, member_data["collection"])
        self.vault = MemberVault(**member_data["vault"])
        self.counts: int = member_data["counts"]
        self.cooldowns = MemberCooldowns(**member_data["cooldowns"])
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
        self._data_version: int = member_data["data_version"]

    def register(self, with_write: bool = False):
        members_dict[self.id] = self
        if self not in members:
            members.append(self)
        if with_write:
            self.write_data()

    async def fetch_discord_user(self, bot: commands.Bot):
        if self._discord_user is None:
            self._discord_user = bot.get_user(self.id)
            if self._discord_user is None:
                self._discord_user = await bot.fetch_user(self.id)

    @property
    def snapshot_data(self) -> Optional[dict[str, Union[str, int]]]:
        if self._discord_user is None:
            return None
        return {
            "id": str(self.id),
            "display_name": self._discord_user.display_name,
            "avatar_url": self._discord_user.display_avatar.replace(size=256).url,
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
            "data_version": self._data_version,
            "balance": self.balance,
            "bank_balance": self._bank_balance,
            "inventory": self.inventory.item_ids,
            "collection": self.collection.item_ids,
            "vault": self.vault.data,
            "counts": self.counts,
            "cooldowns": self.cooldowns.data,
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

    def upload_data(self, force_upload: bool = False, snapshot: Optional[dict] = None, write: bool = True) -> str:
        if force_upload or self.snapshot_has_changed:
            if snapshot is None:
                snapshot = self.snapshot_data
            if snapshot is None:
                return "Snapshot is None"
            Handlers.firestoreHandler.upload_data(snapshot)
            if write:
                self.write_snapshot(snapshot)
            return f"Success - {self._discord_user.display_name}#{self._discord_user.discriminator}"

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
        del members_dict[self.id]
        members.remove(self)


def get(member_id: int) -> Member:
    member = members_dict.get(member_id)
    if member is None:
        member = Member(get_default_values())
        member.id = member_id
        member.register(with_write=True)

    return member


def get_default_values() -> dict:
    with open (f"data/static/members/default_values.json", "r") as infile:
        return json.load(infile)


def load_member_files() -> None:
    members_dict.clear()
    for filename in Utils.get_dir_filepaths(_MEMBERS_DIRECTORY, ".json"):
        with open(filename, "r") as infile:
            data = json.load(infile)
            member = Member(data)
            member.register()


for path in REQUIRED_PATHS:
    Utils.FileChecker.directory(path)

members_dict: dict[int, Member] = {}
members: list[Member] = []
load_member_files()
