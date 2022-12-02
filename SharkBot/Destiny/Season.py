from datetime import datetime, timedelta
import json


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
        seconds = int(self.time_remaining.total_seconds())
        days, seconds = seconds // (24 * 60 * 60), seconds % (24 * 60 * 60)
        hours, seconds = seconds // (60 * 60), seconds % (60 * 60)
        minutes, seconds = seconds // 60, seconds % 60

        output_string = ""
        if days != 0:
            if days == 1:
                output_string += f"{days} day, "
            else:
                output_string += f"{days} days, "
        if hours != 0:
            if hours == 1:
                output_string += f"{hours} hour, "
            else:
                output_string += f"{hours} hours, "
        if minutes != 0:
            if minutes == 1:
                output_string += f"{minutes} minute, "
            else:
                output_string += f"{minutes} minutes, "
        if output_string == "":
            if seconds == 1:
                output_string += f"{seconds} second "
            else:
                output_string += f"{seconds} seconds "
        else:
            output_string = output_string[:-2] + f" and {seconds} "
            if seconds == 1:
                output_string += f"second "
            else:
                output_string += f"seconds "

        return output_string


with open("data/static/destiny/current_season.json", "r") as infile:
    data = json.load(infile)

Season.current = Season(**data)
