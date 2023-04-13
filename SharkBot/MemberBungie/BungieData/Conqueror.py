import discord

from .BungieData import BungieData
from ..ProfileResponseData import ProfileResponseData
import SharkBot
from SharkBot.Destiny import Definitions

cutoff = len("Grandmaster: ")
conqueror_node = Definitions.DestinyPresentationNodeDefinition.get("3776992251")
record_definitions = [
    Definitions.DestinyRecordDefinition.get(record["recordHash"]) for record in conqueror_node["children"]["records"]
]


class Conqueror(BungieData):
    _COMPONENTS = [900]
    _THUMBNAIL_URL = f"https://www.bungie.net{conqueror_node['displayProperties']['icon']}"

    @staticmethod
    def _process_data(data: ProfileResponseData):
        records = data["profileRecords"]["data"]["records"]
        results: list[dict[str, str | bool]] = []
        for record_definition in record_definitions:
            record_data = records[str(record_definition["hash"])]
            try:
                complete = all([objective["complete"] for objective in record_data["objectives"]])
            except KeyError:
                complete = all([objective["complete"] for objective in record_data["intervalObjectives"]])
            results.append({
                "name": record_definition["displayProperties"]["name"],
                "description": record_definition["displayProperties"]["description"],
                "forTitleGilding": record_definition["forTitleGilding"],
                "complete": complete
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
    def _format_embed_data(embed: discord.Embed, data: list[dict[str, str | bool]], **kwargs):
        title_gilded = all([record["complete"] for record in data if not record["forTitleGilding"]])
        incomplete: list[dict[str, str | bool]] = [
            record for record in data if record["forTitleGilding"] == title_gilded and not record["complete"]
        ]
        if len(incomplete) == 0:
            embed.description = f"You have completed Conqueror this season!"
            return
        if title_gilded:
            embed.description = f"You have {len(incomplete)} GMs to complete this season!"
            for record in incomplete:
                nightfall_name = record["name"][cutoff:]
                nightfall = SharkBot.Destiny.Nightfall.get(nightfall_name).grandmaster
                embed.add_field(
                    name=nightfall_name,
                    value=nightfall.icons_str,
                    inline=False
                )
        else:
            embed.description = f"You have {len(incomplete)} Objectives left to complete!"
            for record in incomplete:
                embed.add_field(
                    name=record["name"],
                    value=record["description"],
                    inline=False
                )
