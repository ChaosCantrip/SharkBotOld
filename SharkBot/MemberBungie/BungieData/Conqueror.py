import discord

from .BungieData import BungieData
import SharkBot

conqueror_definitions: dict[str, str] = SharkBot.Utils.JSON.load("data/static/bungie/definitions/Conqueror.json")


class Conqueror(BungieData):
    _COMPONENTS = [900]
    _THUMBNAIL_URL = None

    @staticmethod
    def _process_data(data):
        records = data["profileRecords"]["data"]["records"]
        result: dict[str, bool] = {}
        for record_hash, nightfall_name in conqueror_definitions.items():
            record_data = records[record_hash]
            complete = all([objective["complete"] for objective in record_data["objectives"]])
            result[nightfall_name] = complete
        return result

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
