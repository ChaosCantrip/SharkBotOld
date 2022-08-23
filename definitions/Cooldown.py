from datetime import datetime, timedelta

timeFormat = "%S:%M:%H/%d:%m:%Y"


class Cooldown:

    def __init__(self, name: str):
        self.name = name
