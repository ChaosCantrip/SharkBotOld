import random
import os


def roll_probability(probability: int) -> bool:
    return random.randint(0, probability) == probability


def get_dir_filepaths(dir: str) -> list[str]:
    return [f"{dir}/{filename}" for filename in os.listdir(dir)]
