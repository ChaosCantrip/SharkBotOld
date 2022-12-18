import secret
import aiohttp


async def upload_counts(data: list[list]):
    payload = {
        "members": {
            str(d[0]): {
                "member_id": d[0],
                "member_name": d[1],
                "counts": d[2]
            } for d in data
        }
    }
    async with aiohttp.ClientSession() as session:
        async with session.put(
            url=f"{secret.SharkBotAPI.base_uri}/upload_multi",
            json=payload,
            headers=secret.SharkBotAPI.auth_header
        ) as response:
            if response.status != 201:
                print("Fuck")
