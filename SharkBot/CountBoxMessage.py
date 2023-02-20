import SharkBot

_MESSAGES_FILEPATH = "data/live/bot/CountBoxMessages.json"

SharkBot.Utils.FileChecker.json(
    _MESSAGES_FILEPATH,
    default_value={
        "886721016766799882": "Hey, would you look at that! You found an [ITEM]"
    }
)

class CountBoxMessage:
    messages: dict[str, str] = SharkBot.Utils.JSON.load(_MESSAGES_FILEPATH)