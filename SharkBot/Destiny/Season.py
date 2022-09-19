from datetime import datetime, timedelta


class Season:

    def __init__(self, name: str, number: int, start: str, end: str, icon: str) -> None:
        self.name = name
        self.number = number
        self.start = datetime.strptime(start, "%d/%m/%Y")
        self.start += timedelta(hours=18)
        self.end = datetime.strptime(end, "%d/%m/%Y")
        self.end += timedelta(hours=18)
        self.icon = icon

