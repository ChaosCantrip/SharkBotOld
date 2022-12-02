from datetime import datetime, timedelta
import json

from SharkBot import Utils


class Season:
    current = None

    def __init__(self, name: str, number: int, start: str, end: str, icon: str) -> None:
        self.name = name
        self.number = number
        self.start = datetime.strptime(start, "%d/%m/%Y")
        self.start += timedelta(hours=18)
        self.end = datetime.strptime(end, "%d/%m/%Y")
        self.end += timedelta(hours=18)
        self.icon = icon

    @property
    def calendar_string(self) -> str:
        return f"{datetime.strftime(self.start, '%d %b')} - {datetime.strftime(self.end, '%d %b')}"

    @property
    def time_remaining(self) -> timedelta:
        return self.end - datetime.now()

    @property
    def time_remaining_string(self) -> str:
        return Utils.td_to_string(self.time_remaining)


with open("data/static/destiny/current_season.json", "r") as infile:
    data = json.load(infile)

Season.current = Season(**data)
