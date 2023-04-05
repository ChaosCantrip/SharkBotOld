import aiohttp
import secret


async def make_request(messages: list[str]) -> tuple[int, dict]:
    async with aiohttp.ClientSession() as session:
        async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers=secret.OpenAI.API_HEADERS,
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [{
                        "role": "user",
                        "content": message
                    } for message in messages],
                }
        ) as resp:
            return resp.status, await resp.json()
