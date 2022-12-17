import secret
import aiohttp


async def upload_counts(member_id: int, member_name: str, counts: int):
    async with aiohttp.ClientSession() as session:
        async with session.put(
            url=f"{secret.SharkBotAPI.base_uri}/upload_count",
            json={
                "member_id": member_id,
                "member_name": member_name,
                "counts": counts
            },
            headers=secret.SharkBotAPI.auth_header
        ) as response:
            if response.status != 201:
                print("Fuck")
