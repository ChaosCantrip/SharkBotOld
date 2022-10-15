import random
import os


def roll_probability(probability: int) -> bool:
    return random.randint(0, probability) == probability


def get_dir_filepaths(directory: str) -> list[str]:
    """
    Returns a list of all files in the directory, including the path to the directory

    :param directory: Directory to be listed
    """
    return [f"{directory}/{filename}" for filename in os.listdir(directory)]