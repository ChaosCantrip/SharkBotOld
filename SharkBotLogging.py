import os
from datetime import datetime
import logging

if not os.path.isdir("data/live/bot/logs"):
    os.makedirs("data/live/bot/logs")

LOG_FORMAT_DICT = {
    "source": "SharkBot",
    "time": "%(asctime)s",
    "level": "%(levelname)s",
    "logger": "%(name)s",
    "message": "%(message)s"
}


CURRENT_LOGFILE = f"data/live/bot/logs/{int(datetime.utcnow().timestamp())}.log"

logging.basicConfig(
    filename=CURRENT_LOGFILE,
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logging.info("SharkBot Logging Initialised")
