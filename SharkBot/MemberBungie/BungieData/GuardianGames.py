import discord

from .BungieData import BungieData
from ..ProfileResponseData import ProfileResponseData
import SharkBot

ROOT_STRIKE_QUEST = SharkBot.Destiny.Definitions.DestinyInventoryItemDefinition.get(151874009)
STRIKE_QUEST_HASHES = [step["itemHash"] for step in ROOT_STRIKE_QUEST["setData"]["itemList"]]
ROOT_CRUCIBLE_QUEST = SharkBot.Destiny.Definitions.DestinyInventoryItemDefinition.get(3491245264)
CRUCIBLE_QUEST_HASHES = [step["itemHash"] for step in ROOT_CRUCIBLE_QUEST["setData"]["itemList"]]
ROOT_STRIKE_DESCRIPTION = ROOT_STRIKE_QUEST["displayProperties"]["description"].split("\n")[-1]
ROOT_CRUCIBLE_DESCRIPTION = ROOT_CRUCIBLE_QUEST["displayProperties"]["description"].split("\n")[-1]
STRIKE_RANK_HASH = ROOT_STRIKE_DESCRIPTION[ROOT_STRIKE_DESCRIPTION.index("{var:") + 5:ROOT_STRIKE_DESCRIPTION.index("}")]
CRUCIBLE_RANK_HASH = ROOT_CRUCIBLE_DESCRIPTION[ROOT_CRUCIBLE_DESCRIPTION.index("{var:") + 5:ROOT_CRUCIBLE_DESCRIPTION.index("}")]
MEDAL_CASE = SharkBot.Destiny.Definitions.DestinyInventoryItemDefinition.get(3734389316)


class GuardianGames(BungieData):
    _COMPONENTS = [1200, 202]
    _THUMBNAIL_URL = f"https://www.bungie.net{MEDAL_CASE['displayProperties']['icon']}"
    _EMBED_TITLE = "Guardian Games"
    _EMBED_COLOUR = discord.Colour.light_gray()

    @staticmethod
    def _process_data(data: ProfileResponseData):
        item_objectives = {}
        for character_id, character_data in data["characterProgressions"]["data"].items():
            item_objectives |= character_data["uninstancedItemObjectives"]
        strike_score = 0
        crucible_score = 0
        for item_hash, objectives in item_objectives.items():
            if int(item_hash) in STRIKE_QUEST_HASHES:
                strike_score = max(strike_score, max(objective["progress"] for objective in objectives))
            elif int(item_hash) in CRUCIBLE_QUEST_HASHES:
                crucible_score = max(crucible_score, max(objective["progress"] for objective in objectives))
        return {
            "strike_score": strike_score,
            "strike_rank": data["profileStringVariables"]["data"]["integerValuesByHash"][STRIKE_RANK_HASH],
            "crucible_score": crucible_score,
            "crucible_rank": data["profileStringVariables"]["data"]["integerValuesByHash"][CRUCIBLE_RANK_HASH]
        }

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
    def _format_embed_data(embed: discord.Embed, data, **kwargs):
        embed.add_field(
            name="Vanguard Operations",
            value=f"**Score**: {data['strike_score']:,}\n**Rank**: Top {data['strike_rank']}%",
        )
        embed.add_field(
            name="Supremacy",
            value=f"**Score**: {data['crucible_score']:,}\n**Rank**: Top {data['crucible_rank']}%",
        )
