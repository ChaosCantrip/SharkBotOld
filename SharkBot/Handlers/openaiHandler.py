from typing import TypedDict
import aiohttp
import secret


class Prompt(TypedDict):
    role: str
    content: str


SHARKBOT_PROMPT = Prompt(
    role="system",
    content="You are SharkBot, an AI Bot that is designed to give fun and interesting responses. You can use discord markdown and emojis to make your responses look better."
)


async def make_request(messages: list[dict]) -> tuple[int, dict]:
    async with aiohttp.ClientSession() as session:
        async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers=secret.OpenAI.API_HEADERS,
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": messages
                }
        ) as resp:
            return resp.status, await resp.json()


async def ask_sharkbot(message: str) -> tuple[int, dict]:
    return await make_request([SHARKBOT_PROMPT, {"role": "user", "content": message}])