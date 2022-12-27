import shutil
import os
from datetime import datetime, timedelta, date
from typing import Optional

from SharkBot.Errors import ZIPBackup as Errors


def create_backup(dt: Optional[date]):
    if dt is None:
        dt = datetime.now().date()
    shutil.make_archive(f"data/live/backups/{dt}", "zip", "data/live/members")
