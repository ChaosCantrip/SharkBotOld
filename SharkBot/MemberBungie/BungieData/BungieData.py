import os.path
from typing import Optional, Any
import discord
from discord.ext import commands

import SharkBot

_PARENT_CACHE_FOLDER = "data/live/bungie/cache"

class BungieData:
    _COMPONENTS = [0]
    _LOADING_ICON_URL = "https://cdn.dribbble.com/users/2081/screenshots/4645074/loading.gif"

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

    # Embeds

    def generate_cache_embed(self, ctx: commands.Context) -> discord.Embed:
        embed = discord.Embed(
            title=f"Fetching {self.__name__} Data...",
            description="Data may be outdated until I fetch the updated data.",
        )
        embed.set_thumbnail(url=self._LOADING_ICON_URL)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        cached_data = self.get_cache()
        if cached_data is not None:
            self._format_embed_data(embed, cached_data)
        return embed