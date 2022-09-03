from datetime import datetime, timedelta
from definitions import Item, SharkErrors
from typing import Union


class Mission:

    def __init__(self, id: str, name: str, description: str, action: str, quota: int, duration: timedelta, reward: Item.Item):
        self.id = id
        self.name = name
        self.description = description
        self.action = action
        self.quota = quota
        self.duration = duration
        self.reward = reward


class MemberMission:

    def __init__(self, member, missionid: str, progress: int, resetsOn: datetime, claimed: bool):
        self.member = member
        self.mission = get(missionid)
        self._progress = progress
        self.resetsOn = resetsOn
        self._claimed = claimed

    @property
    def progress(self) -> int:
        self.verify_reset()
        return self._progress

    @progress.setter
    def progress(self, value: int) -> None:
        self.verify_reset()
        if value > self.mission.quota:
            self._progress = value
        elif value < 0:
            self._progress = 0
        else:
            self._progress = value
        self.member.write_data()

    def verify_reset(self) -> None:
        if self.expired:
            self.reset()

    def reset(self) -> None:
        self.resetsOn = datetime.now().date() - ((datetime.now().date() - self.resetsOn) % self.mission.duration)
        self.resetsOn += self.mission.duration
        self._progress = 0
        self._claimed = False
        self.member.write_data()

    @property
    def expired(self) -> bool:
        return datetime.now().date() < self.resetsOn

    @property
    def completed(self) -> bool:
        self.verify_reset()
        return self.progress == self.mission.quota

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
        self.member.write_data()


class MemberMissions:

    def __init__(self, member, data):
        self.missions = [MemberMission(member, m["missionid"], m["progress"], m["resetsOn"], m["claimed"]) for m in data]

    def get(self, missionid: str) -> MemberMission:
        for mission in self.missions:
            if mission.id == missionid:
                return mission
        raise SharkErrors.MissionNotFoundError(missionid)

    def get_of_type(self, type: str) -> list[MemberMission]:
        return [mission for mission in self.missions if mission.type == type]


missions = [
    Mission(
        id="dailyCount",
        name="Daily Count",
        description="Count 3 times a day",
        action="count",
        quota=3,
        duration=timedelta(days=1),
        reward=Item.get("LOOT1")
    ),
    Mission(
        id="weeklyCount",
        name="Weekly Count",
        description="Count 10 times a week",
        action="count",
        quota=10,
        duration=timedelta(weeks=1),
        reward=Item.get("LOOT5")
    )
]


def get(missionid: str) -> Mission:
    for mission in missions:
        if mission.id == missionid:
            return mission
    raise SharkErrors.MissionNotFoundError(missionid)
