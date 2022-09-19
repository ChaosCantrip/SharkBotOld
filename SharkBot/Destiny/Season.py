from datetime import datetime, timedelta
import json


class Season:

    def __init__(self, name: str, number: int, description: str, start: str, end: str, icon: str) -> None:
        self.name = name
        self.number = number
        self.description = description
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
        seconds = int(self.time_remaining.total_seconds())
        days, seconds = seconds // (24 * 60 * 60), seconds % (24 * 60 * 60)
        hours, seconds = seconds // (60 * 60), seconds % (60 * 60)
        minutes, seconds = seconds // 60, seconds % 60

        outputString = ""
        if days != 0:
            if days == 1:
                outputString += f"{days} day, "
            else:
                outputString += f"{days} days, "
        if hours != 0:
            if hours == 1:
                outputString += f"{hours} hour, "
            else:
                outputString += f"{hours} hours, "
        if minutes != 0:
            if minutes == 1:
                outputString += f"{minutes} minute, "
            else:
                outputString += f"{minutes} minutes, "
        if outputString == "":
            if seconds == 1:
                outputString += f"{seconds} second "
            else:
                outputString += f"{seconds} seconds "
        else:
            outputString = outputString[:-2] + f" and {seconds} "
            if seconds == 1:
                outputString += f"second "
            else:
                outputString += f"seconds "

        return outputString


with open("data/static/destiny/current_season.json", "r") as infile:
    data = json.load(infile)

current = Season(**data)