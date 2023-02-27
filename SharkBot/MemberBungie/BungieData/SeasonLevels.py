from dataclasses import dataclass
import discord
from datetime import datetime, timezone

from .BungieData import BungieData
import SharkBot

@dataclass
class SeasonData:
    name: str
    number: int
    level: int

    def __str__(self):
        return f"`{self.number}` {self.name} `Level {self.level}`"

class SeasonLevels(BungieData):
    _COMPONENTS = [104, 202]
    _THUMBNAIL_URL = None

    @staticmethod
    def _process_data(data):
        now = datetime.utcnow().astimezone(timezone.utc)
        result = []
        character_progression = list(data["characterProgressions"]["data"].values())[0]["progressions"]
        for season in SharkBot.Destiny.Season.seasons:
            if season.has_season_pass:
                if season.start > now:
                    continue
                progress = 0
                for h in season.progression_hashes:
                    if str(h) not in character_progression:
                        continue
                    progress += character_progression[str(h)]["level"]
                if progress > 1:
                    result.append(SeasonData(season.name, season.number, progress))
        return result

    @staticmethod
    def _process_cache_write(data):
        return [s.__dict__ for s in data]

    @staticmethod
    def _process_cache_load(data):
        return [SeasonData(**d) for d in data]

    # @classmethod
    # def _format_cache_embed_data(cls, embed: discord.Embed, data, **kwargs):
    #     cls._format_embed_data(embed, data)

    @staticmethod
    def _format_embed_data(embed: discord.Embed, data: list[SeasonData], **kwargs):
        total_num = sum([s.level for s in data])
        embed.description = f"You have gained `{total_num} Levels` over your time in Destiny."
        embed.add_field(
            name="Season Levels",
            value="\n".join(str(s) for s in data)
        )
