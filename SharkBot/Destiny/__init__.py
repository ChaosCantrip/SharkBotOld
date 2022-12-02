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


def get_day_index() -> int:
    dt_now = datetime.utcnow()
    if dt_now.time() > reset_time:
        dt_now -= timedelta(days=1)
    return (dt_now - season_start).days


def get_week_index() -> int:
    return get_day_index() // 7
