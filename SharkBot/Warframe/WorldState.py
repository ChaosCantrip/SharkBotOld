from datetime import datetime
from typing import Literal, Self

import aiohttp

import SharkBot


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

