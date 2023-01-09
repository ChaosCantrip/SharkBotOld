from datetime import timedelta
from typing import Optional
from .Cooldown import Cooldown

class MemberCooldowns:

    def __init__(self, hourly: Optional[str] = None, daily: Optional[str] = None, weekly: Optional[str] = None):
        self.hourly = Cooldown(name="hourly", duration=timedelta(hours=1), expiry=hourly)
        self.daily = Cooldown(name="daily", duration=timedelta(days=1), expiry=daily)
        self.weekly = Cooldown(name="weekly", duration=timedelta(weeks=1), expiry=weekly)