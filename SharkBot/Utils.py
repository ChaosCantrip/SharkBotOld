import random
import os
from typing import Union
import difflib

import discord
import SharkBot


def roll_probability(probability: int) -> bool:
    return random.randint(0, probability) == probability


def get_dir_filepaths(directory: str, extension: Union[str, None] = None) -> list[str]:
    """
    Returns a list of all files in the directory, including the path to the directory

    :param directory: Directory to be listed
    :param extension: (Optional) If defined, only files with this extension are returned
    :return: List of files in the directory including paths
    """
    if extension is None:
        return [f"{directory}/{filename}" for filename in os.listdir(directory)]
    else:
        if extension[0] != ".":
            extension = f".{extension}"
        return [f"{directory}/{filename}" for filename in os.listdir(directory) if filename.endswith(extension)]


def split_embeds(embed: discord.Embed) -> list[discord.Embed]:
    fields = embed.fields
    embed.clear_fields()

    field_texts = []
    for field in fields:
        field_text = ""
        for line in field.value.split("\n"):
            if len(field_text + "\n" + line) > 1000:
                field_texts.append((field.name, field_text[:-1], field.inline))
                field_text = ""
            field_text += f"{line}\n"
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


def get_similar_items(search: str) -> Union[str, None]:
    result = difflib.get_close_matches(
        search,
        ([i.name.upper() for i in SharkBot.Item.items] + [i.id.upper() for i in SharkBot.Item.items]),
        n=1
    )
    return None if len(result) == 0 else result[0]
