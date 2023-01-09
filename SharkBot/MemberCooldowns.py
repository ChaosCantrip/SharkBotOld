from datetime import timedelta
from typing import Optional
from .Cooldown import Cooldown

class MemberCooldowns:

    def __init__(
            self, hourly: Optional[str] = None, daily: Optional[str] = None,
            weekly: Optional[str] = None, event: Optional[str] = None
    ):
        self.hourly = Cooldown(name="hourly", duration=timedelta(hours=1), expiry=hourly)
        self.daily = Cooldown(name="daily", duration=timedelta(days=1), expiry=daily)
        self.weekly = Cooldown(name="weekly", duration=timedelta(weeks=1), expiry=weekly)
        self.event = Cooldown(name="event", duration=timedelta(hours=2), expiry=event)

    @property
    def data(self) -> dict[str, str]:
        return {
            "hourly": self.hourly.data,
            "daily": self.daily.data,
            "weekly": self.weekly.data,
            "event": self.event.data
        }