from datetime import datetime, timedelta
from typing import Union


class Mission:

    def __init__(self, id: str, name: str, description: str, quota: int, duration: timedelta, reward):
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
