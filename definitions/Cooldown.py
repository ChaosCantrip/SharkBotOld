from datetime import datetime, timedelta

timeFormat = "%S:%M:%H/%d:%m:%Y"


class Cooldown:

    def __init__(self, name: str, expiry: str, duration: timedelta) -> None:
        self.name = name
        self.expiry = datetime.strptime(expiry, timeFormat)
        self.duration = duration

    @property
    def expired(self) -> bool:
        return datetime.now() > self.expiry

    def extend(self) -> None:
        self.expiry += self.duration

    def reset(self) -> None:
        self.expiry = datetime.now() + self.duration

    @property
    def timestring(self) -> str:
        return datetime.strftime(self.expiry, timeFormat)

    @property
    def timeremaining(self) -> timedelta:
        return datetime.now() - self.expiry


class NewCooldown:

    def __init__(self, name: str, duration: timedelta) -> None:
        self.name = name
        self.expiry = datetime.now() + duration
        self.duration = duration
