from datetime import datetime, timedelta, date
from typing import Union, TypedDict
import json

import discord
from discord.ext import commands

from SharkBot import Item, Errors, Utils
from SharkBot.Views import MissionCompleteView

dateFormat = "%d/%m/%Y"
types = ["Daily", "Weekly"]


class _MissionData(TypedDict):
    mission_id: str
    name: str
    description: str
    action: str
    quota: int
    mission_type: str
    rewards: list[str]


class Mission:
    missions = []

    def __init__(self, mission_id: str, name: str, description: str, action: str, quota: int, mission_type: str,
                 rewards: list[str]):
        self.id = mission_id
        self.name = name
        self.description = description
        self.action = action
        self.quota = quota
        self.type = mission_type
        if self.type == "Daily":
            self.duration = timedelta(days=1)
        elif self.type == "Weekly":
            self.duration = timedelta(weeks=1)
        else:
            raise Errors.MissionTypeNotFoundError(self.name, self.type)
        self.rewards = list(Item.get(item_id) for item_id in rewards)

    @classmethod
    def get(cls, mission_id: str):
        for mission in cls.missions:
            if mission.id == mission_id:
                return mission
        raise Errors.MissionNotFoundError(mission_id)

    @property
    def raw_data(self) -> dict[str, Union[str, int, list[str]]]:
        """
        Returns data for the mission in the format used in data/statics/missions files.
        Not used, kept in for posterity.

        :return: dict of raw data for the mission
        """
        return {
            "mission_id": self.id,
            "name": self.name,
            "description": self.description,
            "action": self.action,
            "quota": self.quota,
            "mission_type": self.type,
            "rewards": [item.id for item in self.rewards]
        }

    @classmethod
    def dump(cls) -> None:
        """
        Dumps data for all missions into files in data/static/missions.
        Not used, kept in for posterity.
        """

        for mission_type in types:
            missions = [mission for mission in cls.missions if mission.type == mission_type]
            output = [mission.raw_data for mission in missions]

            with open(f"data/static/missions/{mission_type.lower()}.json", "w+") as outfile:
                json.dump(output, outfile, indent=4)

    @classmethod
    def import_missions(cls) -> None:
        """
        Constructs list of available Missions from json files in data/static/missions
        """

        cls.missions = []

        for filepath in Utils.get_dir_filepaths("data/static/missions"):
            with open(filepath, "r") as infile:
                data: list[_MissionData] = json.load(infile)

            for mission_data in data:
                cls.missions.append(Mission(**mission_data))


class MemberMission:

    def __init__(self, member, mission_id: str, progress: int, resets_on: date, claimed: bool):
        self.member = member
        self.mission = Mission.get(mission_id)
        self._progress = progress
        self.resetsOn = resets_on
        self._claimed = claimed

    @property
    def id(self) -> str:
        return self.mission.id

    @property
    def name(self) -> str:
        return self.mission.name

    @property
    def description(self) -> str:
        return self.mission.description

    @property
    def action(self) -> str:
        return self.mission.action

    @property
    def quota(self) -> int:
        return self.mission.quota

    @property
    def type(self) -> str:
        return self.mission.type

    @property
    def duration(self) -> timedelta:
        return self.mission.duration

    @property
    def rewards(self) -> list[Union[Item.Item, Item.Lootbox]]:
        return self.mission.rewards

    @property
    def progress(self) -> int:
        self.verify_reset()
        return self._progress

    @progress.setter
    def progress(self, value: int) -> None:
        self.verify_reset()
        if value > self.quota:
            self._progress = self.quota
        elif value < 0:
            self._progress = 0
        else:
            self._progress = value

    def verify_reset(self) -> None:
        if self.expired:
            self.reset()

    def reset(self) -> None:
        self.resetsOn = datetime.now().date() - ((datetime.now().date() - self.resetsOn) % self.duration)
        self.resetsOn += self.duration
        self._progress = 0
        self._claimed = False

    @property
    def expired(self) -> bool:
        return datetime.now().date() >= self.resetsOn

    @property
    def completed(self) -> bool:
        self.verify_reset()
        return self.progress == self.quota

    @property
    def can_claim(self) -> bool:
        return self.completed and not self._claimed

    @property
    def claimed(self) -> bool:
        self.verify_reset()
        return self._claimed

    @claimed.setter
    def claimed(self, value: bool) -> None:
        self._claimed = value

    def grant_rewards(self) -> None:
        for item in self.rewards:
            self.member.inventory.add(item)
        self.member.write_data()

    def claim_rewards(self) -> None:
        self.claimed = True
        self.member.stats.completedMissions += 1
        self.grant_rewards()

    @property
    def rewards_text(self) -> str:
        return ", ".join([str(item) for item in self.rewards])

    @property
    def data(self) -> dict:
        return {
            "missionid": self.id,
            "progress": self.progress,
            "resetsOn": datetime.strftime(self.resetsOn, dateFormat),
            "claimed": self.claimed
        }


class MemberMissions:

    def __init__(self, member, data):
        self.member = member

        missions_data = {mission.id: None for mission in Mission.missions}

        for missionData in data:
            missions_data[missionData["missionid"]] = missionData

        self.missions = []
        for missionId, missionData in missions_data.items():
            if missionData is None:
                self.missions.append(
                    MemberMission(
                        member=self.member,
                        mission_id=missionId,
                        progress=0,
                        resets_on=datetime(2022, 8, 29).date(),
                        claimed=False
                    )
                )
            else:
                try:
                    self.missions.append(
                        MemberMission(
                            member=self.member,
                            mission_id=missionId,
                            progress=missionData["progress"],
                            resets_on=datetime.strptime(missionData["resetsOn"], dateFormat).date(),
                            claimed=missionData["claimed"]
                        )
                    )
                except Errors.MissionNotFoundError:
                    pass

    def get(self, missionid: str) -> MemberMission:
        for mission in self.missions:
            if mission.id == missionid:
                return mission
        raise Errors.MissionNotFoundError(self.member.id, missionid)

    def get_of_action(self, action: str) -> list[MemberMission]:
        return [mission for mission in self.missions if mission.action == action]

    async def log_action(self, action: str, ctx: commands.Context, amount: int = 1):
        for mission in [mission for mission in self.missions if mission.action == action]:
            mission.progress += amount
            if mission.can_claim:
                mission.claim_rewards()

                embed = discord.Embed()
                embed.title = f"{mission.type} Mission Complete!"
                embed.description = f"{mission.description}"
                embed.colour = discord.Colour.green()
                embed.add_field(
                    name="Rewards!",
                    value=f"You got {mission.rewards_text}!"
                )

                view = MissionCompleteView(mission.rewards, self.member, embed)
                view.message = await ctx.reply(embed=embed, view=view, mention_author=False)

        self.member.write_data()

    async def log_action_small(self, action: str, message: discord.Message, amount: int = 1):
        for mission in [mission for mission in self.missions if mission.action == action]:
            mission.progress += amount
            if mission.can_claim:
                mission.claim_rewards()

                await message.reply(
                    f"{mission.type} Mission Complete - *{mission.description}*\nYou got: {mission.rewards_text}!",
                    mention_author=False
                )

        self.member.write_data()

    @property
    def data(self) -> list[dict]:
        return [mission.data for mission in self.missions]


Mission.import_missions()
