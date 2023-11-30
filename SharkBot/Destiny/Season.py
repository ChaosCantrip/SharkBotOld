from datetime import datetime, timedelta, timezone
import json
from typing import Any, Optional, Self

from SharkBot import Utils
from SharkBot.Destiny import Definitions


class Season:
    seasons: list[Self] = []
    current: Optional[Self] = None

    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data
        self.start: Optional[datetime] = None
        self.end: Optional[datetime] = None
        _start_date = data.get("startDate")
        if _start_date is not None:
            self.start = datetime.fromisoformat(_start_date)
        _end_date = data.get("endDate")
        if _end_date is not None:
            self.end = datetime.fromisoformat(_end_date)
        self.icon_url: Optional[str] = None
        if data["displayProperties"]["hasIcon"]:
            self.icon_url = "https://bungie.net" + data["displayProperties"]["icon"]

    def __getitem__(self, item):
        return self._data[item]

    def get(self, key, default=None):
        return self._data.get(key, default)

    @property
    def name(self) -> str:
        return self._data["displayProperties"]["name"]

    @property
    def description(self) -> str:
        return self._data["displayProperties"]["description"]

    @property
    def number(self) -> int:
        return self._data.get("seasonNumber", -1)

    @property
    def calendar_string(self) -> Optional[str]:
        return f"{datetime.strftime(self.start, '%d %b') if self.start is not None else '???'} - {datetime.strftime(self.end, '%d %b') if self.end is not None else '???'}"

    @property
    def time_remaining(self) -> Optional[timedelta]:
        if self.end is None:
            return None
        return self.end - datetime.utcnow()

    @property
    def time_remaining_string(self) -> Optional[str]:
        if self.end is None:
            return None
        return Utils.td_to_string(self.time_remaining)

    @property
    def has_season_pass(self) -> bool:
        return self._data.get("seasonPassHash") is not None

    @property
    def season_pass_definition(self) -> Optional[dict]:
        if self.has_season_pass:
            return Definitions.DestinySeasonPassDefinition.get(self._data["seasonPassHash"])
        else:
            return None

    @property
    def progression_hashes(self) -> Optional[list[int]]:
        season_pass = self.season_pass_definition
        if season_pass is None:
            return None
        else:
            return [season_pass["rewardProgressionHash"], season_pass["prestigeProgressionHash"]]

    @property
    def artifact_definition(self) -> Optional[dict]:
        artifact_hash = self._data.get("artifactItemHash")
        if artifact_hash is None:
            return None
        else:
            return Definitions.DestinyInventoryItemDefinition.get(artifact_hash)


Season.seasons = [Season(d) for d in Definitions.DestinySeasonDefinition.get_all().values()]
Season.seasons.sort(key=lambda s: s.number)

now = datetime.utcnow().astimezone(timezone.utc)

for season in Season.seasons:
    if season.start is not None and season.end is not None:
        if season.start < now < season.end:
            Season.current = season
            break

if Season.current is None:
    Season.current = Season.seasons[-1]
