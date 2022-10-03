import random


def roll_probability(probability: int) -> bool:
    return random.randint(0, probability) == probability
