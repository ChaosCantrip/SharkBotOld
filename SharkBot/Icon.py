import json
import logging

import discord

import SharkBot.Utils


class Icon:
    _icons: dict[str, str] = {}
    FILEPATH: str = "data/live/icons.json"
    PLACEHOLDER: str = ":anger:"
    LOGGER = logging.getLogger("icon")

    @classmethod
    def get(cls, name: str) -> str:
        return cls._icons.get(name, cls.PLACEHOLDER)

    @classmethod
    def load(cls) -> None:
        cls._icons = {}
        with open(cls.FILEPATH, "r") as infile:
            cls._icons = json.load(infile)

    @classmethod
    def write(cls) -> None:
        with open(cls.FILEPATH, "w") as outfile:
            json.dump(cls._icons, outfile, indent=2)

    @classmethod
    def check(cls, guild: discord.Guild) -> bool:
        cls.LOGGER.info("Checking for new Icons.")
        for emoji in guild.emojis:
            if emoji.name not in cls._icons:
                cls.LOGGER.info(f"New Icon Detected - '<:{emoji.name}:{emoji.id}>'")
                return False
            if cls._icons[emoji.name] != f"<:{emoji.name}:{emoji.id}>":
                cls.LOGGER.info(f"Icon Change Detected - '{cls._icons[emoji.name]}' -> '<:{emoji.name}:{emoji.id}>'")
                return False
        else:
            cls.LOGGER.info(f"No changes detected.")
            return True

    @classmethod
    def extract(cls, guild: discord.Guild) -> None:
        cls._icons = {}
        for emoji in guild.emojis:
            cls._icons[emoji.name] = f"<:{emoji.name}:{emoji.id}>"
        cls.write()
        cls.LOGGER.info(f"Extracted new icons from '{guild.name}'")

    @classmethod
    def icon_dict(cls) -> dict[str, str]:
        return dict(cls._icons)

SharkBot.Utils.FileChecker.json(Icon.FILEPATH, default_value={})
Icon.load()
