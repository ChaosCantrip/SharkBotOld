import json
import os

import discord

Collections = {
    "witch_queen_item": "<:witch_queen_item:1023837957771251772>",
    "exotic_item": "<:exotic_item:964988904035983432>",
    "mythic_item": "<:mythic_item:964988904124084315>",
    "common_item": "<:common_item:964988904371535902>",
    "easter_item": "<:easter_item:964988904388321320>",
    "rare_item": "<:rare_item:964988904421867591>",
    "legendary_item": "<:legendary_item:964988904459604028>",
    "uncommon_item": "<:uncommon_item:964988904535105566>",
    "valentines_item": "<:valentines_item:964996933234073600>",
    "lootboxes_item": "<:lootboxes_item:964996933351538790>",
    "summer_item": "<:summer_item:1012587024248754176>",
    "slime_rancher_item": "<:slime_rancher_item:1023831794602229780>",
    "halloween_item": "<:halloween_item:1030596811758514207>",
    "christmas_item": "<:christmas_item:1047569432689528915>",
    "fragment_item": "<:fragment_item:1051956781359829073>",
    "new_year_item": "<:new_year_item:1056659303660007465>",
    "anniversary_item": "<:anniversary_item:1056645481121448007>"
}


class Icons:
    _icons: dict[str, str] = {}
    _FILEPATH: str = "data/live/icons.json"

    @classmethod
    def get(cls, name: str) -> str:
        if name in cls._icons:
            return cls._icons["name"]
        else:
            return ":anger:"

    @classmethod
    def load(cls) -> None:
        cls._icons = {}
        with open(cls._FILEPATH, "r") as infile:
            cls._icons = json.load(infile)

    @classmethod
    def write(cls) -> None:
        with open(cls._FILEPATH, "w") as outfile:
            json.dump(cls._icons, outfile)

    @classmethod
    def check(cls, guild: discord.Guild) -> bool:
        for emoji in guild.emojis:
            if emoji.name not in cls._icons:
                return False
            if cls._icons != f"<:{emoji.name}:{emoji.id}>":
                return False
        else:
            return True

    @classmethod
    def extract(cls, guild: discord.Guild) -> None:
        cls._icons = {}
        for emoji in guild.emojis:
            cls._icons[emoji.name] = f"<:{emoji.name}:{emoji.id}>"
        cls.write()

    @classmethod
    def ensure_file_exists(cls) -> None:
        if not os.path.exists(cls._FILEPATH):
            with open(cls._FILEPATH, "w+") as newfile:
                json.dump({}, newfile)
