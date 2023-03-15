import discord

from .BungieData import BungieData
import SharkBot

_CLASSES = ["Titan", "Hunter", "Warlock"]
_RACES = ["Human", "Awoken", "Exo"]

class Pinnacles(BungieData):
    _COMPONENTS = [200, 204]
    _THUMBNAIL_URL = None

    @staticmethod
    def _process_data(data) -> dict[str, dict[str, list[str]]]:
        character_data: dict[str, dict] = data["characters"]["data"]
        activity_data: dict[str, dict[str, list[dict]]] = data["characterActivities"]["data"]
        results: dict[str, dict[str, list[str]]] = {}
        for character_hash, character_activities in activity_data.items():
            character_definition = character_data[character_hash]
            character_name = f"{_RACES[character_definition['raceType']]} {_CLASSES[character_definition['classType']]}"

            character_results: dict[str, set[str]] = {}
            for character_activity in character_activities["availableActivities"]:
                if (activity_challenges:=character_activity.get("challenges")) is None:
                    continue
                incomplete_objective_hashes = [challenge["objective"]["objectiveHash"] for challenge in activity_challenges if not challenge["objective"]["complete"]]
                if len(incomplete_objective_hashes) == 0:
                    continue
                activity_definition = SharkBot.Destiny.Definitions.DestinyActivityDefinition.get(character_activity["activityHash"])
                activity_name = activity_definition["displayProperties"]["name"].split(":")[0]
                for activity_challenge in activity_definition["challenges"]:
                    if activity_challenge["objectiveHash"] not in incomplete_objective_hashes:
                        continue
                    for reward in activity_challenge["dummyRewards"]:
                        item_name = SharkBot.Destiny.Definitions.DestinyInventoryItemDefinition.get(reward["itemHash"])["displayProperties"]["name"]
                        if "Gear" not in item_name:
                            continue
                        if item_name not in character_results:
                            character_results[item_name] = set()
                        character_results[item_name].add(activity_name)
            results[character_name] = {reward: list(activities) for reward, activities in character_results.items()}

        return results

    # @staticmethod
    # def _process_cache_write(data: dict[str, dict[str, list[str]]]) -> dict[str, dict[str, list[str]]]:
    #     return data

    # @staticmethod
    # def _process_cache_load(data: dict[str, dict[str, list[str]]]) -> dict[str, dict[str, list[str]]]:
    #     return data

    # @classmethod
    # def _format_cache_embed_data(cls, embed: discord.Embed, data: dict[str, dict[str, list[str]]], **kwargs):
    #     cls._format_embed_data(embed, data)

    # @staticmethod
    # def _format_embed_data(embed: discord.Embed, data: dict[str, dict[str, list[str]]], **kwargs):
    #     embed.description = f"\n```{SharkBot.Utils.JSON.dumps(data)}```"
