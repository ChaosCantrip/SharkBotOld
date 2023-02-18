import discord

from .BungieData import BungieData
import SharkBot

_BOUNTY_REFERENCE: dict[str, list[str]] = SharkBot.Utils.JSON.load("data/static/bungie/definitions/BountiesSorted.json")

_WEEKLY_TARGETS = {
    "Dreaming City": 7,
    "Europa": 4,
    "Clan": 8,
    "Moon": 4,
    "Eternity": 1
}

_RACES = {
    0: "Human",
    1: "Awoken",
    2: "Exo"
}

_CLASSES = {
    0: "Titan",
    1: "Hunter",
    2: "Warlock"
}

class _Guardian:

    def __init__(self, character_data: dict):
        self._race = _RACES[character_data["raceType"]]
        self._class = _CLASSES[character_data["classType"]]

    @property
    def icon(self) -> str:
        return SharkBot.Icon.get(f"class_{self._class}")

    def __str__(self) -> str:
        return f"{self.icon} {self._race} {self._class}"


class BountyPrep(BungieData):
    _COMPONENTS = [200,201,301]
    _EMBED_COLOUR = discord.Colour.blue()
    _EMBED_TITLE = "Bounty Prep Progress"

    @staticmethod
    def _process_data(data):
        character_data: dict[str, dict] = data["characters"]["data"]
        character_inventories_data: dict[str, dict[str, list[dict]]] = data["characterInventories"]["data"]
        objective_data: dict[str, dict[str, list[dict]]] = data["itemComponents"]["objectives"]["data"]
        result = {}
        for character_hash, inventory_data in character_inventories_data.items():
            guardian = _Guardian(character_data[character_hash])
            processed_data = {
                "Total": 0,
                "Weekly": {
                    "Clan": 0,
                    "Dreaming City": 0,
                    "Europa": 0,
                    "Moon": 0,
                    "Eternity": 0
                },
                "Vanguard": 0,
                "Crucible": 0,
                "Gambit": 0,
                "Daily": 0,
                "Gunsmith": 0,
                "Repeatable": 0,
                "Useless": [],
                "Incomplete": []
            }
            for item_data in inventory_data["items"]:
                bounty_data = _BOUNTY_REFERENCE.get(str(item_data["itemHash"]))
                if bounty_data is None:
                    continue
                bounty_instance = objective_data[item_data["itemInstanceId"]]
                processed_data["Total"] += 1
                bounty_type, bounty_source, bounty_name = bounty_data
                bounty_complete = all([objective["complete"] for objective in bounty_instance["objectives"]])
                if not bounty_complete:
                    if bounty_type not in ["Repeatable", "Useless"]:
                        processed_data["Incomplete"].append([bounty_name, bounty_source])
                        continue
                if bounty_type == "Weekly":
                    processed_data["Weekly"][bounty_source] = processed_data["Weekly"].get(bounty_source, 0) + 1
                elif bounty_type == "Useless":
                    processed_data["Useless"].append([bounty_name, bounty_source])
                else:
                    processed_data[bounty_type] += 1
            result[f"{guardian} `({processed_data['Total']}/63)`"] = processed_data
        return result

    @staticmethod
    def _format_embed_data(embed: discord.Embed, data):
        for character_title, character_data in data.items():
            output_text = ["**Weekly**"]
            extra_weeklies = 0
            for source, num in character_data["Weekly"].items():
                target_num = _WEEKLY_TARGETS.get(source)
                if target_num is None:
                    extra_weeklies += num
                    output_text.append(f"- {source}: `{num}`")
                else:
                    output_text.append(f"- {source}: `{num}/{target_num}`")
            for source in ["Vanguard", "Crucible", "Gambit"]:
                output_text.append(f"**{source}**: `{character_data[source]}/8`")
            output_text.append(f"**Daily**: `{character_data['Daily']}/{15-extra_weeklies}`")
            if len(character_data["Incomplete"]) > 0:
                output_text.append("\n**__Incomplete Bounties:__**")
                for bounty_name, bounty_source in character_data["Incomplete"]:
                    output_text.append(f"**{bounty_source}** {bounty_name}")
            trash_text = []
            if character_data["Gunsmith"] > 0:
                trash_text.append(f"**Gunsmith**: `{character_data['Gunsmith']}`")
            if character_data["Repeatable"] > 0:
                trash_text.append(f"**Repeatable**: `{character_data['Repeatable']}`")
            if len(character_data["Useless"]) > 0:
                trash_text.append(f"\n**Useless Bounties**: `{len(character_data['Useless'])}`")
                for bounty_name, bounty_source in character_data["Useless"]:
                    trash_text.append(f"- {bounty_name} ({bounty_source})")

            if len(trash_text) > 0:
                output_text.append("\t__Trash__")
                output_text.extend(trash_text)

            embed.add_field(
                name=f"__{character_title}__",
                value="\n".join(output_text)
            )
        embed.set_footer(text="This checklist was composed from mine and Luke's work, there is no way to customise it <3")