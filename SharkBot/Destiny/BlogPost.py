import aiohttp
from datetime import datetime

from SharkBot import Utils
import secret


class BlogPost:

    def __init__(self, response_data: dict[str, str]):
        self.title = response_data["Title"]
        self.link = f"https://www.bungie.net{response_data['Link']}"
        self.publish_date = datetime.fromisoformat(response_data["PubDate"])
        self.id = response_data["UniqueIdentifier"]
        self.description = response_data["Description"]
        self.image = response_data.get("ImagePath")
        self.mobile_image = response_data.get("OptionalMobileImagePath")