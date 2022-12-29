import json
import os
import discord


class Icon:
    _icons: dict[str, str] = {}
    _FILEPATH: str = "data/live/icons.json"
    PLACEHOLDER: str = ":anger:"

    @classmethod
    def get(cls, name: str) -> str:
        return cls._icons.get(name, cls.PLACEHOLDER)

    @classmethod
    def load(cls) -> None:
        cls._icons = {}
        cls.ensure_file_exists()
        with open(cls._FILEPATH, "r") as infile:
            cls._icons = json.load(infile)

    @classmethod
    def write(cls) -> None:
        with open(cls._FILEPATH, "w") as outfile:
            json.dump(cls._icons, outfile, indent=2)

    @classmethod
    def check(cls, guild: discord.Guild) -> bool:
        for emoji in guild.emojis:
            if emoji.name not in cls._icons:
                return False
            if cls._icons[emoji.name] != f"<:{emoji.name}:{emoji.id}>":
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

    @classmethod
    def icon_dict(cls) -> dict[str, str]:
        return dict(cls._icons)


Icon.load()
