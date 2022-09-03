from datetime import datetime, timedelta
from definitions import Item, SharkErrors
from typing import Union


class Mission:

    def __init__(self, id: str, name: str, description: str, quota: int, duration: timedelta, reward: Item.Item):
        self.id = id
        self.name = name
        self.description = description
        self.quota = quota
        self.duration = duration
        self.reward = reward


class MemberMission:

    def __init__(self, member, missionid: str, progress: int, resetsOn: datetime):
        self.member = member
        self.mission = get(missionid)
        self.progress = progress
        self.resetsOn = resetsOn


class MemberMissions:
    pass


missions = [
    Mission(
        id="dailyCount",
        name="Daily Count",
        description="Count 3 times a day",
        quota=3,
        duration=timedelta(days=1),
        reward=Item.get("LOOT1")
    ),
    Mission(
        id="weeklyCount",
        name="Weekly Count",
        description="Count 10 times a week",
        quota=10,
        duration=timedelta(weeks=1),
        reward=Item.get("LOOT5")
    )
]
