import SharkBot

_PARENT_CACHE_FOLDER = "data/live/bungie/cache"

class BungieData:

    @classmethod
    def _cache_folder_path(cls) -> str:
        return f"{_PARENT_CACHE_FOLDER}/{cls.__name__.lower()}"