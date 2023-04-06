from typing import Optional

import aiohttp
from datetime import datetime

from SharkBot import Utils
import secret


class BlogPost:

    def __init__(self, response_data: dict[str, str]):
        self.title = response_data.get("Title")
        self.link = f"https://www.bungie.net{response_data.get('Link')}"
        self.publish_date = datetime.fromisoformat(response_data["PubDate"])
        self.id = response_data.get("UniqueIdentifier")
        self.description = response_data.get("Description")
        self.image = response_data.get("ImagePath")
        self.mobile_image = response_data.get("OptionalMobileImagePath")

    @property
    def thumbnail_url(self) -> Optional[str]:
        return self.image or self.mobile_image
