import os.path
from typing import Optional, Any

import SharkBot

_PARENT_CACHE_FOLDER = "data/live/bungie/cache"

class BungieData:
    _COMPONENTS = [0]

    def __init__(self, member):
        self.member: SharkBot.Member.Member = member

    @classmethod
    def _cache_folder_path(cls) -> str:
        return f"{_PARENT_CACHE_FOLDER}/{cls.__name__.lower()}"

    @property
    def _cache_file(self) -> str:
        return f"{self._cache_folder_path()}/{self.member.id}.json"

    def get_cache(self) -> Optional[Any]:
        if os.path.isfile(self._cache_file):
            return SharkBot.Utils.JSON.load(self._cache_file)
        else:
            return None

    def write_cache(self, data):
        SharkBot.Utils.JSON.dump(self._cache_file, data)