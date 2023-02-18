from typing import Optional

from .BungieData import BungieData
import SharkBot
import discord

_monument_hashes = SharkBot.Utils.JSON.load("data/static/bungie/definitions/ExoticArchiveSorted.json")

class Monument(BungieData):
    _COMPONENTS = [800]
    _EMBED_TITLE = "Monument to Lost Light"

    @staticmethod
    def _process_data(data):
        profile_data = data["profileCollectibles"]["data"]["collectibles"]
        character_data = list(data["characterCollectibles"]["data"].values())[0]["collectibles"]
        output = {}
        for year_num, year_data in _monument_hashes.items():
            _data = {}
            for weapon_hash, weapon_name in year_data.items():
                if weapon_hash in profile_data:
                    state = profile_data[weapon_hash]["state"]
                else:
                    state = character_data[weapon_hash]["state"]
                _data[weapon_name] = state == 0
            output[year_num] = _data
        return output

    @staticmethod
    def _format_embed_data(embed: discord.Embed, data, years: Optional[list[str]] =None, **kwargs):
        output = {}
        for year_num, year_data in data.items():
            data = []
            if year_num not in years:
                continue
            for weapon_name, owned in year_data.items():
                if not owned:
                    data.append(f"- {weapon_name}")
            output[year_num] = data
        for year_num, data in output.items():
            if len(data) == 0:
                embed.add_field(
                    name=f"__**Year {year_num}**__",
                    value=f"*You have finished all your **Year {year_num}** Exotics!*",
                    inline=False
                )
            else:
                embed.add_field(
                    name=f"__**Year {year_num}**__",
                    value="\n".join(data),
                    inline=False
                )