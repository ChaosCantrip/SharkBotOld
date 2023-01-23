from typing import Self
from datetime import datetime, timedelta
from SharkBot import Item

_TIME_FORMAT = "%d/%m/%Y"

class EventCalendar:
    event_calendars: list[Self] = []

    def __init__(self, start_date: str, item_list: list[str]):
        self.start_date = datetime.strptime(start_date, _TIME_FORMAT).date()
        self.end_date = self.start_date + timedelta(days=len(item_list))
        self.items = [Item.get(item_id) for item_id in item_list]