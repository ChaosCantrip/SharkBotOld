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
    bonus: int

def bonus_to_xp(bonus: int) -> int:
    return ((bonus-2) * 110000) + 55000

def xp_to_bonus(xp: int) -> int:
    bonus = 1
    total_xp = 0
    while True:
        total_xp += bonus_to_xp(bonus+1)
        if total_xp > xp:
            return bonus
        else:
            bonus += 1

class SeasonLevels(BungieData):
    _COMPONENTS = [202]
    _THUMBNAIL_URL = None
    _EMBED_TITLE = "Season Levels"
    _EMBED_COLOUR = discord.Colour.dark_gold()

    @staticmethod
    def _process_data(data):
        now = datetime.utcnow().astimezone(timezone.utc)
        result = []
        character_progression = list(data["characterProgressions"]["data"].values())[0]["progressions"]
        for season in SharkBot.Destiny.Season.seasons:
            if season.has_season_pass:
                if season.start > now:
                    continue
                level = 0
                xp = 0
                for h in season.progression_hashes:
                    if str(h) not in character_progression:
                        continue
                    level += character_progression[str(h)]["level"]
                    xp += character_progression[str(h)]["currentProgress"]
                if level > 1:
                    result.append(SeasonData(season.name, season.number, level, xp_to_bonus(xp)))
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
        for s in data:
            embed.add_field(
                name=f"__Season {s.number}__",
                value=f"**{s.name}**\nLevel: `{s.level}`\nPower Bonus: `+{s.bonus}`",
                inline=False
            )
        embed.set_thumbnail(
            url="https://bungie.net" + SharkBot.Destiny.Season.current.artifact_definition["displayProperties"]["icon"]
        )
