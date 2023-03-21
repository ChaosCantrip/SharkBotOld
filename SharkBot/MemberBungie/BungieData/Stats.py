from datetime import datetime

import discord

from .BungieData import BungieData
import SharkBot

STATS_DICT = {
    stat.name.title(): str(stat.value) for stat in SharkBot.Destiny.Enums.GuardianStats
}

_padding_width = max(len(stat_name) for stat_name in STATS_DICT.keys()) + 5

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

    @staticmethod
    def _format_embed_data(embed: discord.Embed, data: list[dict[str, int | str | dict[str, int]]], **kwargs):
        for guardian_data in data:
            guardian = SharkBot.Destiny.Guardian(guardian_data)
            stat_lines = [f"`{stat_name.ljust(_padding_width)}{str(stat_value).ljust(4)}`" for stat_name, stat_value in guardian_data["stats"].items()]
            stat_lines.append(f"\n`{'Tiers'.ljust(_padding_width)}{guardian_data['tiers']}  `")
            embed.add_field(
                name=f"__{guardian.race} {guardian.type}__ `{guardian_data['light']}`",
                value="\n".join(stat_lines)
            )
