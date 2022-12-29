import json
import os
import discord


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
        cls.ensure_file_exists()
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


Icons.load()
