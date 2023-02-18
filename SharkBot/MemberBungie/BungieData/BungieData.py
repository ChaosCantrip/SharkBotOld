import os.path
from typing import Optional, Any

import SharkBot

_PARENT_CACHE_FOLDER = "data/live/bungie/cache"

class BungieData:
    _COMPONENTS = [0]

    def __init__(self, member):
        self.member: SharkBot.Member.Member = member
        self._cached_data: Optional[Any] = None

    # Change in Subclass

    @staticmethod
    def _process_data(data):
        return data

    @staticmethod
    def _process_cache_write(data):
        return data

    @staticmethod
    def _process_cache_load(data):
        return data

    @staticmethod
    def _format_embed_data(embed: discord.Embed, data):
        embed.description += f"\n```{SharkBot.Utils.JSON.dumps(data)}```"

    # Caching Methods

    @classmethod
    def _cache_folder_path(cls) -> str:
        return f"{_PARENT_CACHE_FOLDER}/{cls.__name__.lower()}"

    @property
    def _cache_file(self) -> str:
        return f"{self._cache_folder_path()}/{self.member.id}.json"

    def get_cache(self) -> Optional[Any]:
        if self._cached_data is None:
            if os.path.isfile(self._cache_file):
                self._cached_data = self._process_cache_load(SharkBot.Utils.JSON.load(self._cache_file))
        return self._cached_data

    def write_cache(self, data):
        self._cached_data = data
        SharkBot.Utils.JSON.dump(self._cache_file, self._process_cache_write(data))

    def wipe_cache(self):
        if os.path.isfile(self._cache_file):
            os.remove(self._cache_file)

    # Data Fetching

    async def fetch_data(self, write_cache: bool = True):
        data = await self.member.bungie.get_profile_response(*self._COMPONENTS)
        data = self._process_data(data)
        if write_cache:
            self.write_cache(data)
        return data
