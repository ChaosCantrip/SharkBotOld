import json
import random
import os
import traceback
from datetime import timedelta
from typing import Optional
import difflib
import humanize
import colorama
import discord
from discord.ext import commands

import SharkBot


def get_dir_filepaths(directory: str, extension: Optional[str] = None) -> list[str]:
    """
    Returns a list of all files in the directory, including the path to the directory

    :param directory: Directory to be listed
    :param extension: (Optional) If defined, only files with this extension are returned
    :return: List of files in the directory including paths
    """
    if extension is None:
        return [f"{directory}/{filename}" for filename in os.listdir(directory)]
    else:
        if not extension.startswith("."):
            extension = f".{extension}"
        return [f"{directory}/{filename}" for filename in os.listdir(directory) if filename.endswith(extension)]


def split_embeds(embed: discord.Embed, split: str = "\n") -> list[discord.Embed]:
    fields = embed.fields
    embed.clear_fields()

    field_texts = []
    for field in fields:
        field_text = ""
        for line in field.value.split(split):
            if len(field_text + split + line) > 1000:
                field_texts.append((field.name, field_text[:-1], field.inline))
                field_text = ""
            field_text += f"{line}{split}"
        field_texts.append((field.name, field_text[:-1], field.inline))

    for name, value, inline in field_texts:
        if len(embed) + len(name) + len(value) > 5500 or len(embed.fields) == 25:
            yield embed
            embed.clear_fields()
        embed.add_field(
            name=name,
            value=value,
            inline=inline
        )
    yield embed


def get_similar_items(search: str, cutoff: float = 0.6) -> Optional[str]:
    result = difflib.get_close_matches(
        search,
        ([i.name.upper() for i in SharkBot.Item.items] + [i.id.upper() for i in SharkBot.Item.items]),
        n=1,
        cutoff=cutoff
    )
    return None if len(result) == 0 else result[0]


def get_similar_collections(search: str) -> Optional[str]:
    collections = SharkBot.Collection.collections
    result = difflib.get_close_matches(
        search,
        ([c.name.upper() for c in collections] + [c.id.upper() for c in collections]),
        n=1
    )
    return None if len(result) == 0 else result[0]


def td_to_string(time_remaining: timedelta) -> str:
    return humanize.precisedelta(time_remaining, format="%0.0f")


async def task_loop_handler(bot, error: Exception):

    error_type = type(error)
    print(f"{error_type.__module__}.{error_type.__name__}{error.args}")
    error_name = f"{error_type.__module__}.{error_type.__name__}{error.args}"

    dev = await bot.fetch_user(SharkBot.IDs.dev)
    embed = discord.Embed()
    embed.title = "Task Error Report"
    embed.description = "Oopsie Woopsie Oopsie Woopsie"
    embed.add_field(name="Type", value=error_name, inline=False)
    embed.add_field(name="Args", value=error.args, inline=False)
    embed.add_field(name="Traceback", value="\n".join(traceback.format_tb(error.__traceback__)))
    await dev.send(embed=embed)

    raise error

class FileChecker:

    @classmethod
    def directory(cls, path: str):
        if not os.path.isdir(path):
            os.makedirs(path)
            print(colorama.Fore.YELLOW + colorama.Style.BRIGHT + f"Created Directory: '{path}'")

    @classmethod
    def file(cls, path: str, default_value: str = ""):
        if not os.path.isfile(path):
            directory = os.path.split(path)[0]
            if directory != "":
                cls.directory(directory)
            with open(path, "w+") as outfile:
                outfile.write(default_value)
                print(colorama.Fore.YELLOW + colorama.Style.BRIGHT + f"Created File: '{path}'")

    @classmethod
    def json(cls, path: str, default_value, indent: int = 2):
        if not os.path.isfile(path):
            directory = os.path.split(path)[0]
            if directory != "":
                cls.directory(directory)
            with open(path, "w+") as outfile:
                json.dump(default_value, outfile, indent=indent)
                print(colorama.Fore.YELLOW + colorama.Style.BRIGHT + f"Created JSON: '{path}'")


class JSON:

    @staticmethod
    def load(filepath: str):
        with open(filepath, "r") as _infile:
            return json.load(_infile)

    @staticmethod
    def dump(filepath: str, data, indent: int = 2):
        try:
            with open(filepath, "w+") as _outfile:
                json.dump(data, _outfile, indent=indent)
        except FileNotFoundError:
            FileChecker.json(filepath, data)

class Embed:

    @staticmethod
    def send(embed: discord.Embed, ctx: commands.Context):
        for e in split_embeds(embed):
            await ctx.send(embed=e)

    @staticmethod
    def reply(embed: discord.Embed, message: discord.Message, mention_author: bool = False):
        for e in split_embeds(embed):
            await message.reply(embed=e, mention_author=mention_author)

