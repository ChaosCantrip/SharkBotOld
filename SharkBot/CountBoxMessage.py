from typing import Optional

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
    def get(cls, member_id: int, num: int) -> Optional[str]:
        member_id = str(member_id)
        num = str(num)
        if member_id not in cls._messages_dict:
            return None
        else:
            return cls._messages_dict[member_id].get(num)

    @classmethod
    def remove(cls, member_id: int, num: int):
        text = cls.get(member_id, num)
        member_id = str(member_id)
        num = str(num)
        cls._messages.remove(text)
        del cls._messages_dict[member_id][num]
        cls._messages_dict[member_id] = {
            str(i+1): old_text for i, old_text in enumerate(cls._messages_dict[member_id].values())
        }
        SharkBot.Utils.JSON.dump(_MESSAGES_FILEPATH, cls._messages_dict)

    @classmethod
    def add(cls, member_id: int, text: str):
        if text.lower() in [t.lower() for t in cls._messages]:
            raise SharkBot.Errors.CountBoxMessageExistsError(member_id, text)
        member_id = str(member_id)
        if member_id not in cls._messages_dict:
            cls._messages_dict[member_id] = {}
        num = str(len(cls._messages_dict[member_id]) + 1)
        cls._messages_dict[member_id][num] = text
        cls._messages.append(text)
        SharkBot.Utils.JSON.dump(_MESSAGES_FILEPATH, cls._messages_dict)


    @classmethod
    def use_random(cls, response: SharkBot.Response.InventoryAddResponse):
        return f"**{str(response)}**".join(random.choice(cls._messages).split("[ITEM]"))

CountBoxMessage.load()