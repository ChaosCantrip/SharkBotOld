import random
import os
from typing import Union

import discord


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
    embeds = [embed.copy()]
    embeds[-1].clear_fields()

    for field in embed.fields:
        if len(embeds[-1]) + len(field.name) + len(field.value) > 5500 or len(embeds[-1].fields) == 25:
            embeds.append(embed.copy())
            embeds[-1].clear_fields()
        embeds[-1].add_field(
            name=field.name,
            value=field.value,
            inline=field.inline
        )

    return embeds
