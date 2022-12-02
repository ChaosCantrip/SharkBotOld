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


def get_current_day() -> date:
    dtnow = datetime.utcnow()
    if dtnow.time() < reset_time:
        dtnow -= timedelta(days=1)
    return dtnow.date()
