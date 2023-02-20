import SharkBot
import random

_MESSAGES_FILEPATH = "data/live/bot/CountBoxMessages.json"

SharkBot.Utils.FileChecker.json(
    _MESSAGES_FILEPATH,
    default_value={
        "886721016766799882": {
            "1": "Hey, would you look at that! You found [ITEM]"
        }
    }
)

class CountBoxMessage:
    _messages_dict: dict[str, dict[str, str]] = {}
    _messages: list[str] = []

    @classmethod
    def load(cls):
        cls._messages_dict = SharkBot.Utils.JSON.load(_MESSAGES_FILEPATH)
        cls._messages.clear()
        for message_dict in cls._messages_dict.values():
            cls._messages.extend(message_dict.values())

    @classmethod
    def use_random(cls, item: SharkBot.Item.Item):
        return f"**{str(item)}**".join(random.choice(cls._messages).split("[ITEM]"))


