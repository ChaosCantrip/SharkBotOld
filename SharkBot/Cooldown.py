from datetime import datetime, timedelta

from SharkBot import Utils

timeFormat = "%d/%m/%Y-%H:%M:%S"


class Cooldown:

    def __init__(self, name: str, expiry: str, duration: timedelta) -> None:
        self.name = name
        self.expiry = datetime.strptime(expiry, timeFormat)
        self.duration = duration

    @property
    def expired(self) -> bool:
        return datetime.utcnow() > self.expiry

    def extend(self) -> None:
        self.expiry += self.duration

    def reset(self) -> None:
        self.expiry = datetime.utcnow() + self.duration

    @property
    def timestring(self) -> str:
        return datetime.strftime(self.expiry, timeFormat)

    @property
    def time_remaining(self) -> timedelta:
        return self.expiry - datetime.utcnow()

    @property
    def time_remaining_string(self) -> str:
        return Utils.td_to_string(self.time_remaining)
