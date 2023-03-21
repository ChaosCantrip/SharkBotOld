from datetime import datetime

import discord

from .BungieData import BungieData
import SharkBot

STATS_DICT = {
    stat.name.title(): str(stat.value) for stat in SharkBot.Destiny.Enums.GuardianStats
}

class Stats(BungieData):
    _COMPONENTS = [200]
    _THUMBNAIL_URL = None

    @staticmethod
    def _process_data(data) -> list[dict[str, int | str | dict[str, int]]]:
        results: list[dict[str, int | str | dict[str, int]]] = []
        for guardian_data in sorted(data["characters"]["data"].values(),
                key=lambda d: datetime.fromisoformat(d["dateLastPlayed"]), reverse=True):
            guardian_stats = {
                stat_name: guardian_data["stats"][stat_hash] for stat_name, stat_hash in STATS_DICT.items()
            }
            tiers = sum(stat // 10 for stat in guardian_stats.values())
            results.append({
                "raceType": guardian_data["raceType"],
                "classType": guardian_data["classType"],
                "light": guardian_data["light"],
                "stats": guardian_stats,
                "tiers": tiers
            })
        return results

    # @staticmethod
    # def _process_cache_write(data):
    #     return data

    # @staticmethod
    # def _process_cache_load(data):
    #     return data

    # @classmethod
    # def _format_cache_embed_data(cls, embed: discord.Embed, data, **kwargs):
    #     cls._format_embed_data(embed, data)

    # @staticmethod
    # def _format_embed_data(embed: discord.Embed, data, **kwargs):
    #     embed.description = f"\n```{SharkBot.Utils.JSON.dumps(data)}```"
