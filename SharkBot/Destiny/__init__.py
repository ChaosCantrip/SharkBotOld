from datetime import timedelta, time, datetime

from . import Errors
from .Champion import Champion
from .Shield import Shield
from .Difficulty import Difficulty
from .LostSectorReward import LostSectorReward
from .LostSector import LostSector
from .Season import Season
from .Raid import Raid
from .Dungeon import Dungeon
from .Nightfall import Nightfall
from . import Reset
from .ComponentTypeEnum import ComponentTypeEnum
from .Wellspring import Wellspring

from SharkBot.Cooldown import Cooldown as _Cooldown

lightfall_countdown = _Cooldown(
    name="Lightfall Cooldown",
    expiry="28/02/2023-18:00:00",
    duration=timedelta(days=356)
)

reset_time = time(hour=17)  # UTC time
season_start = datetime(2022, 12, 6)


def is_past_reset() -> bool:
    dt_now = datetime.utcnow()
    return dt_now.time() > reset_time


def is_weekly_reset() -> bool:
    dt_now = datetime.utcnow()
    if dt_now.weekday() == 1 and is_past_reset():
        return True
    elif dt_now.weekday() == 2 and not is_past_reset():
        return True
    else:
        return False


def get_last_reset() -> datetime:
    dt_now = datetime.utcnow().replace(
        hour=reset_time.hour,
        minute=reset_time.minute,
        second=reset_time.second,
        microsecond=reset_time.microsecond
    )
    if not is_past_reset():
        dt_now = dt_now - timedelta(days=1)
    return dt_now


def get_day_index(relative_to: datetime = season_start) -> int:
    dt_now = datetime.utcnow()
    if dt_now.time() < reset_time:
        dt_now -= timedelta(days=1)
    return (dt_now - relative_to).days


def get_week_index(relative_to: datetime = season_start) -> int:
    return get_day_index(relative_to) // 7
