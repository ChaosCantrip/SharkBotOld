import json

from SharkBot import Item

with open("data/static/collectibles/advent.json") as infile:
    advent_data = json.load(infile)


def get_day(day: int) -> Item:
    return Item.get(advent_data[day-1])
