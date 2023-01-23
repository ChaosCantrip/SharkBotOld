import json
import os.path
from typing import Self, Optional
from datetime import datetime, timedelta, date
from SharkBot import Item, Utils, Member

_DATE_FORMAT = "%d/%m/%Y"
_SOURCE_FILE = "data/static/collectibles/event_calendars.json"
_TRACKING_FOLDER = "data/static/live/event_calendars"
Utils.FileChecker.directory(_TRACKING_FOLDER)

class EventCalendar:
    event_calendars: list[Self] = []
    _current_calendar: Optional[Self] = None
    _last_checked_date: date = datetime.now().date() - timedelta(days=1)

    def __init__(self, name: str, start_date: str, item_list: list[str]):
        self.name = name
        self._tracking_file = f"{_TRACKING_FOLDER}/{self.name}.json"
        self.start_date = datetime.strptime(start_date, _DATE_FORMAT).date()
        self.end_date = self.start_date + timedelta(days=len(item_list))
        self.items = [Item.get(item_id) for item_id in item_list]
        self.member_tracker: dict[Member.Member, int] = {}

        if os.path.isfile(self._tracking_file):
            with open(self._tracking_file, "r") as infile:
                _tracking_data = json.load(infile)
            self.member_tracker = {
                Member.get(member_id): tracked_index
                for member_id, tracked_index in _tracking_data.items()
            }

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

    def get_reward(self, index: Optional[int] = None) -> Item.Item:
        if index is None:
            index = self.get_current_index()
        return self.items[index]

    def write_member_tracker(self) -> None:
        with open(self._tracking_file, "w+") as _outfile:
            json.dump(self.member_tracker, _outfile, indent=2)

    def member_can_claim(self, member: Member.Member, index: Optional[int] = None) -> bool:
        if index is None:
            index = self.get_current_index()

        if member in self.member_tracker:
            return self.member_tracker[member] < index
        else:
            return True

    def mark_member_claimed(self, member: Member.Member, index: Optional[int] = None) -> None:
        if index is None:
            index = self.get_current_index()

        self.member_tracker[member] = index
        self.write_member_tracker()

