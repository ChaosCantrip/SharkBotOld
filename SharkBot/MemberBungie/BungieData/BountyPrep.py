from .BungieData import BungieData
import SharkBot

_BOUNTY_REFERENCE: dict[str, list[str]] = SharkBot.Utils.JSON.load("data/static/bungie/definitions/BountiesSorted.json")

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