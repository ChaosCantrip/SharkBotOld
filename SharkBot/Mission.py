from datetime import datetime, timedelta, date

from SharkBot.Views import MissionCompleteView
from SharkBot import Item, Errors
from typing import Union
import discord

dateFormat = "%d/%m/%Y"
types = ["Daily", "Weekly"]


class Mission:

    def __init__(self, missionID: str, name: str, description: str, action: str, quota: int, missionType: str,
                 rewards: list[Item.Item]):
        self.id = missionID
        self.name = name
        self.description = description
        self.action = action
        self.quota = quota
        self.type = missionType
        if self.type == "Daily":
            self.duration = timedelta(days=1)
        elif self.type == "Weekly":
            self.duration = timedelta(weeks=1)
        else:
            raise Errors.MissionTypeNotFoundError(self.name, self.type)
        self.rewards = rewards


class MemberMission:

    def __init__(self, member, missionID: str, progress: int, resetsOn: date, claimed: bool):
        self.member = member
        self.mission = get(missionID)
        self._progress = progress
        self.resetsOn = resetsOn
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
        return ", ".join([item.text for item in self.rewards])

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

        missionsData = {mission.id: None for mission in missions}

        for missionData in data:
            missionsData[missionData["missionid"]] = missionData

        self.missions = []
        for missionId, missionData in missionsData.items():
            if missionData is None:
                self.missions.append(
                    MemberMission(
                        member=self.member,
                        missionID=missionId,
                        progress=0,
                        resetsOn=datetime(2022, 8, 29).date(),
                        claimed=False
                    )
                )
            else:
                self.missions.append(
                    MemberMission(
                        member=self.member,
                        missionID=missionId,
                        progress=missionData["progress"],
                        resetsOn=datetime.strptime(missionData["resetsOn"], dateFormat).date(),
                        claimed=missionData["claimed"]
                    )
                )

    def get(self, missionid: str) -> MemberMission:
        for mission in self.missions:
            if mission.id == missionid:
                return mission
        raise Errors.MissionNotFoundError(self.member.id, missionid)

    def get_of_action(self, action: str) -> list[MemberMission]:
        return [mission for mission in self.missions if mission.action == action]

    async def log_action(self, action: str, user: discord.Member):
        for mission in [mission for mission in self.missions if mission.action == action]:
            mission.progress += 1
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
                await user.send(embed=embed, view=view)
        self.member.write_data()

    @property
    def data(self) -> list[dict]:
        return [mission.data for mission in self.missions]


missions = [
    Mission(
        missionID="dailyClaim1",
        name="Daily Claim 1x",
        description="Claim rewards using $claim once a day",
        action="claim",
        quota=1,
        missionType="Daily",
        rewards=[Item.get("LOOTC")]
    ),
    Mission(
        missionID="dailyClaim3",
        name="Daily Claim 3x",
        description="Claim rewards using $claim three times in a day",
        action="claim",
        quota=3,
        missionType="Daily",
        rewards=[Item.get("LOOTU")]
    ),
    Mission(
        missionID="dailyCount5",
        name="Daily Count 5x",
        description="Count 5 times",
        action="count",
        quota=5,
        missionType="Daily",
        rewards=[Item.get("LOOTU")]
    ),
    Mission(
        missionID="dailyCount10",
        name="Daily Count 10x",
        description="Count 10 times",
        action="count",
        quota=10,
        missionType="Daily",
        rewards=[Item.get("LOOTR")]
    ),
    Mission(
        missionID="dailyCoinflip1",
        name="Daily Coinflip 1x",
        description="Perform a coinflip using $coinflip",
        action="coinflip",
        quota=1,
        missionType="Daily",
        rewards=[Item.get("LOOTC")]
    ),
    Mission(
        missionID="weeklyClaim10",
        name="Weekly Claim 10x",
        description="Claim rewards 10 times using $claim",
        action="claim",
        quota=10,
        missionType="Weekly",
        rewards=[Item.get("LOOTSHARK")]
    ),
    Mission(
        missionID="weeklyClaim15",
        name="Weekly Claim 15x",
        description="Claim rewards 15 times using $claim",
        action="claim",
        quota=15,
        missionType="Weekly",
        rewards=[Item.get("LOOTL")]
    ),
    Mission(
        missionID="weeklyCount25",
        name="Weekly Count 25x",
        description="Count 25 times",
        action="count",
        quota=25,
        missionType="Weekly",
        rewards=[Item.get("LOOTSHARK")]
    ),
    Mission(
        missionID="weeklyCount50",
        name="Weekly Count 50x",
        description="Count 50 times",
        action="count",
        quota=50,
        missionType="Weekly",
        rewards=[Item.get("LOOTL")]
    ),
    Mission(
        missionID="weeklyCoinflip5",
        name="Weekly Coinflip 5x",
        description="Perform a coinflip 5 times using $coinflip",
        action="coinflip",
        quota=5,
        missionType="Weekly",
        rewards=[Item.get("LOOTSHARK")]
    ),
    Mission(
        missionID="weeklyCoinflip10",
        name="Weekly Coinflip 10x",
        description="Perform a coinflip 10 times using $coinflip",
        action="coinflip",
        quota=10,
        missionType="Weekly",
        rewards=[Item.get("LOOTL")]
    )
]


def get(missionid: str) -> Mission:
    for mission in missions:
        if mission.id == missionid:
            return mission
    raise Errors.MissionNotFoundError(missionid)
