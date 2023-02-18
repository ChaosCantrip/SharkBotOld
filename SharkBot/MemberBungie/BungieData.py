import SharkBot

_PARENT_CACHE_FOLDER = "data/live/bungie/cache"

class BungieData:

    def __init__(self, member):
        self.member: SharkBot.Member.Member = member

    @classmethod
    def _cache_folder_path(cls) -> str:
        return f"{_PARENT_CACHE_FOLDER}/{cls.__name__.lower()}"

    @property
    def _cache_file(self) -> str:
        return f"{self._cache_folder_path()}/{self.member.id}.json"