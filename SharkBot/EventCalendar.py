from typing import Self, Optional
from datetime import datetime, timedelta, date
from SharkBot import Item

_TIME_FORMAT = "%d/%m/%Y"

class EventCalendar:
    event_calendars: list[Self] = []
    _current_calendar: Optional[Self] = None
    _last_checked_date: date = datetime.now().date() - timedelta(days=1)

    def __init__(self, name: str, start_date: str, item_list: list[str]):
        self.name = name
        self.start_date = datetime.strptime(start_date, _TIME_FORMAT).date()
        self.end_date = self.start_date + timedelta(days=len(item_list))
        self.items = [Item.get(item_id) for item_id in item_list]

    @classmethod
    def get_current(cls) -> Optional[Self]:
        current_date = datetime.now().date()
        if current_date == cls._last_checked_date:
            return cls._current_calendar

        for event_calendar in cls.event_calendars:
            if event_calendar.start_date < current_date < event_calendar.end_date:
                cls._current_calendar = event_calendar
                break
        else:
            cls._current_calendar = None

        cls._last_checked_date = current_date
        return cls._current_calendar

    def get_current_index(self) -> int:
        current_date = datetime.now().date()
        return (current_date - self.start_date).days

    def get_reward(self, n: Optional[int] = None) -> Item.Item:
        if n is None:
            n = self.get_current_index()
        return self.items[n]

