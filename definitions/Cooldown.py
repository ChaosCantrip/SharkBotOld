from datetime import datetime, timedelta

timeFormat = "%S:%M:%H/%d:%m:%Y"


class Cooldown:

    def __init__(self, name: str, expiry: str, duration: timedelta):
        self.name = name
        self.expiry = datetime.strptime(expiry, timeFormat)
        self.duration = timedelta

    @property
    def expired(self):
        return datetime.now() > self.expiry

    def extend(self):
        self.expiry += self.duration

    def reset(self):
        self.expiry = datetime.now() + self.duration

    @property
    def timestring(self):
        return datetime.strftime(self.expiry, timeFormat)


class NewCooldown:

    def __init__(self, name: str, expiry: datetime, duration: timedelta):
        self.name = name
        self.expiry = expiry
        self.duration = duration
