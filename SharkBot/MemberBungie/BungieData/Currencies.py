from .BungieData import BungieData
import SharkBot
import discord

_CURRENCY_HASHES: dict[str, str] = SharkBot.Utils.JSON.load("data/static/bungie/definitions/CurrencyHashes.json")

_CURRENCY_ORDER = [
    "Glimmer",
    "Bright Dust",
    "Legendary Shards",
    "Enhancement Core",
    "Enhancement Prism",
    "Ascendant Shard",
    "Upgrade Module",
    "Ascendant Alloy",
    "Resonant Alloy",
    "Strange Coin"
]

class Currencies(BungieData):
    _COMPONENTS = [600]
    _THUMBNAIL_URL = "https://www.sharkbot.online/images/currency_gif.gif"

    @staticmethod
    def _process_data(data):
        currency_data = data["characterCurrencyLookups"]["data"]
        result_data = {item_name: 0 for item_name in _CURRENCY_ORDER}
        for character_data in currency_data.values():
            quantities = character_data["itemQuantities"]
            for item_hash, quantity in quantities.items():
                item_name = _CURRENCY_HASHES.get(item_hash)
                if item_name is None:
                    continue
                else:
                    result_data[item_name] += quantity

        result = {}
        for item_name, quantity in result_data.items():
            icon_name = SharkBot.Icon.get("currency_" + "_".join(item_name.lower().split(" ")))
            result[f"{icon_name} {item_name}"] = int(quantity/3)
        return result

    @staticmethod
    def _format_embed_data(embed: discord.Embed, data):
        embed.description = "\n".join(f"**{name}** `{qty:,}`" for name, qty in data.items())