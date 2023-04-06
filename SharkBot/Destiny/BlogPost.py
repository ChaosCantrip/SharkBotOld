from typing import Optional, Self

import aiohttp
from datetime import datetime

import discord

from SharkBot import Errors, Utils
import secret


_LAST_PUBLISH_DATE_FILEPATH = "data/live/bungie/last_publish_date.txt"
Utils.FileChecker.file(_LAST_PUBLISH_DATE_FILEPATH, "2023-04-01T00:00:00Z")
with open(_LAST_PUBLISH_DATE_FILEPATH, "r") as f:
    _last_publish_date = datetime.fromisoformat(f.read())


class BlogPost:

    def __init__(self, response_data: dict[str, str]):
        self.title = response_data["Title"]
        self.link = f"https://www.bungie.net{response_data['Link']}"
        self.publish_date = datetime.fromisoformat(response_data["PubDate"])
        self.id = response_data["UniqueIdentifier"]
        self.description = response_data["Description"]
        self.image = response_data.get("ImagePath")
        self.mobile_image = response_data.get("OptionalMobileImagePath")

    @property
    def thumbnail_url(self) -> Optional[str]:
        return self.image or self.mobile_image

    @classmethod
    async def fetch_new_posts(cls) -> list[Self]:
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                "https://www.bungie.net/Platform/Content/Rss/NewsArticles/0/",
                headers={
                    "X-API-Key": secret.BungieAPI.X_API_Key
                }
            )
            if not response.ok:
                raise Errors.BungieAPI.InternalServerError(response.status, response.reason)
            else:
                response_data = await response.json()
                blog_posts = [
                    cls(post_data) for post_data in response_data["Response"]["NewsArticles"]
                ]
                blog_posts.sort(key=lambda post: post.publish_date, reverse=True)
                return [post for post in blog_posts if post.publish_date > _last_publish_date]

    @classmethod
    def update_last_publish_date(cls, new_date: datetime):
        global _last_publish_date
        _last_publish_date = new_date
        with open(_LAST_PUBLISH_DATE_FILEPATH, "w") as _f:
            _f.write(new_date.isoformat())

    def to_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title=self.title,
            description=self.description,
            url=self.link,
            timestamp=self.publish_date
        )
        if self.thumbnail_url:
            embed.set_thumbnail(url=self.thumbnail_url)
        return embed

