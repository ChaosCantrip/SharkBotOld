import json

Collections = {
    "witch_queen_item": "<:witch_queen_item:1023837957771251772>",
    "exotic_item": "<:exotic_item:964988904035983432>",
    "mythic_item": "<:mythic_item:964988904124084315>",
    "common_item": "<:common_item:964988904371535902>",
    "easter_item": "<:easter_item:964988904388321320>",
    "rare_item": "<:rare_item:964988904421867591>",
    "legendary_item": "<:legendary_item:964988904459604028>",
    "uncommon_item": "<:uncommon_item:964988904535105566>",
    "valentines_item": "<:valentines_item:964996933234073600>",
    "lootboxes_item": "<:lootboxes_item:964996933351538790>",
    "summer_item": "<:summer_item:1012587024248754176>",
    "slime_rancher_item": "<:slime_rancher_item:1023831794602229780>",
    "halloween_item": "<:halloween_item:1030596811758514207>",
    "christmas_item": "<:christmas_item:1047569432689528915>",
    "fragment_item": "<:fragment_item:1051956781359829073>",
    "new_year_item": "<:new_year_item:1056659303660007465>",
    "anniversary_item": "<:anniversary_item:1056645481121448007>"
}

icons_filepath = "data/live/icons.json"


class Icons:
    _icons: dict[str, str] = {}

    @classmethod
    def get(cls, name: str) -> str:
        if name in cls._icons:
            return cls._icons["name"]
        else:
            return ":anger:"

    @classmethod
    def load_icons(cls):
        cls._icons = {}
        with open(icons_filepath, "r") as infile:
            cls._icons = json.load(infile)

    @classmethod
    def write_icons(cls):
        with open(icons_filepath, "w") as outfile:
            json.dump(cls._icons, outfile)
