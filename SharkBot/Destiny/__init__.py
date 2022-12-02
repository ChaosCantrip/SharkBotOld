from datetime import timedelta, time, datetime, date

from . import Errors
from . import Champion
from . import Shield
from . import LostSectorReward
from . import LostSector
from . import Season
from . import Raid
from . import Dungeon
from . import Nightfall

from SharkBot.Cooldown import Cooldown as _Cooldown

lightfall_countdown = _Cooldown(
    name="Lightfall Cooldown",
    expiry="28/02/2023-18:00:00",
    duration=timedelta(days=356)
)

reset_time = time(hour=17)  # UTC time
season_start = datetime(2022, 9, 13)


def is_past_reset() -> bool:
    dt_now = datetime.utcnow()
    return dt_now.time() > reset_time


def get_day_index() -> int:
    dt_now = datetime.utcnow()
    if dt_now.time() > reset_time:
        dt_now -= timedelta(days=1)
    return (dt_now - season_start).days


def get_week_index() -> int:
    dt_now = datetime.utcnow()
    if dt_now.time() > reset_time:
        dt_now -= timedelta(days=1)
    return (dt_now - season_start).days // 7
