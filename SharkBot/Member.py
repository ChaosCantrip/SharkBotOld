import json
import os
from datetime import datetime, timedelta
from typing import Union, Optional
import discord
from discord.ext import commands
import logging

import secret
from SharkBot import MemberCooldowns, MemberInventory, MemberCollection, MemberVault, Mission, MemberStats, Utils, XP, Errors, IDs, Handlers, MemberDataConverter, MemberSnapshot, MemberEffects, MemberBungie, Item

BIRTHDAY_FORMAT = "%d/%m/%Y"
_MEMBERS_DIRECTORY = "data/live/members"

member_logger = logging.getLogger("member")

class Member:

    def __init__(self, member_data: dict) -> None:

        data_changed, member_data = MemberDataConverter.convert(member_data)

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
        self.stats = MemberStats(**member_data["stats"])
        self.last_claimed_advent: int = member_data["last_claimed_advent"]
        self.xp = XP(member_data["xp"], self)
        self.legacy: dict = member_data["legacy"]
        self.used_codes: list[str] = member_data["used_codes"]
        self.discord_user: Optional[discord.User] = None
        self._data_version: int = member_data["data_version"]
        self.snapshot = MemberSnapshot(self)
        self.times_uploaded: int = 0
        self.effects = MemberEffects(member_data["effects"])
        self.bungie = MemberBungie(self, **member_data["bungie"])
        self._display_name: Optional[str] = member_data["display_name"]
        self._avatar_url: Optional[str] = member_data["avatar_url"]

        if data_changed:
            self.write_data()

    def register(self, with_write: bool = False):
        members_dict[self.id] = self
        if self not in members:
            members.append(self)
        if with_write:
            self.write_data()

    async def fetch_discord_user(self, bot: commands.Bot, force_get: bool = True, force_fetch: bool = True):
        force_get = force_get or force_fetch
        if self.discord_user is None or force_get:
            self.discord_user = bot.get_user(self.id)
            if self.discord_user is None or force_fetch:
                self.discord_user = await bot.fetch_user(self.id)

    @property
    def raw_display_name(self) -> Optional[str]:
        if self.discord_user is None:
                return self._display_name
        else:
            return self.discord_user.display_name

    @property
    def display_name(self) -> str:
        name = self.raw_display_name
        if name is None:
            return "Exorcised Shark"
        else:
            return name

    @property
    def avatar_url(self) -> Optional[str]:
        if self.discord_user is None:
            return self._avatar_url
        else:
            return self.discord_user.display_avatar.replace(size=256).url

    def view_of_item(self, item: Item.Item):
        if item in self.collection:
            return item
        else:
            return Item.FakeItem(item)

    @property
    def wiki_profile_url(self) -> str:
        return f"https://sharkbot.online/profile/{self.id}"

    def write_data(self, upload: bool = True) -> None:
        """
        Saves the Member data to the .json
        :param upload: Whether to upload the data to Firestore
        """

        member_logger.info(f"{self.id} {self.raw_display_name} - write_data")

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
            "used_codes": self.used_codes,
            "effects": self.effects.data,
            "bungie": self.bungie.data,
            "display_name": self.raw_display_name,
            "avatar_url": self.avatar_url
        }

        with open(f"{_MEMBERS_DIRECTORY}/{self.id}.json", "w") as outfile:
            json.dump(member_data, outfile, indent=4)

        if upload:
            self.upload_data()

    def upload_data(self, force_upload: bool = False, snapshot: Optional[dict] = None, write: bool = True) -> str:
        if force_upload or self.snapshot.has_changed:
            if snapshot is None:
                snapshot = self.snapshot.get_current()
            if snapshot is None:
                return "Snapshot is None"
            if not secret.testBot:
                Handlers.firestoreHandler.upload_member_data(snapshot)
            self.times_uploaded += 1
            if write:
                self.snapshot.write(snapshot)
            return f"Success - {self.display_name}"

    def has_effect(self, effect_id: str) -> bool:
        return self.effects.effect_is_active(effect_id)

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
        os.remove(self.snapshot.path)
        del members_dict[self.id]
        members.remove(self)


def get(member_id: int) -> Member:
    member = members_dict.get(member_id)
    if member is None:
        member_data = get_default_values()
        member_data["id"] = member_id
        member = Member(member_data)
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


Utils.FileChecker.directory(_MEMBERS_DIRECTORY)

members_dict: dict[int, Member] = {}
members: list[Member] = []
load_member_files()
