from datetime import datetime, timedelta
from typing import Literal, Self

import aiohttp

import SharkBot


class LandscapeCycle:

    def __init__(self, data: dict):
        self._data = data

    @property
    def id(self) -> str:
        return self._data["id"]

    @property
    def activation(self) -> datetime:
        return datetime.fromisoformat(self._data["activation"])

    @property
    def expiry(self) -> datetime:
        return datetime.fromisoformat(self._data["expiry"])

    @property
    def expires_in(self) -> timedelta:
        return self.expiry - datetime.utcnow()

    @property
    def state(self) -> str:
        return self._data["state"]


class WorldState:

    def __init__(self, data: dict):
        self._data = data
        self._timestamp = datetime.utcnow()

    @classmethod
    async def get_current(cls, platform: Literal["pc", "ps4", "xb1", "swi"] = "pc") -> Self:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.warframestat.us/{platform}") as response:
                if response.ok:
                    return cls(await response.json())
                else:
                    raise SharkBot.Errors.WarframeAPI.InternalServerError(response, await response.text())


    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    def earth_cycle(self) -> LandscapeCycle:
        return LandscapeCycle(self._data["earthCycle"])

    @property
    def cetus_cycle(self) -> LandscapeCycle:
        return LandscapeCycle(self._data["cetusCycle"])

    @property
    def vallis_cycle(self) -> LandscapeCycle:
        return LandscapeCycle(self._data["vallisCycle"])

    @property
    def cambion_cycle(self) -> LandscapeCycle:
        return LandscapeCycle(self._data["cambionCycle"])

