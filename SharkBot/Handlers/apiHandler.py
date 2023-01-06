from typing import Union

import secret
import aiohttp


async def upload_data(data: dict[str, dict[str, Union[str, int]]]):
    if secret.testBot:
        return
    for member_id, member_data in data.items():
        payload = {
            "member_id": member_id,
            "data": {
                key: value for key, value in member_data.items()
            }
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=f"{secret.SharkBotAPI.base_uri}/member/edit",
                json=payload,
                headers=secret.SharkBotAPI.auth_header
            ) as response:
                return response.status
