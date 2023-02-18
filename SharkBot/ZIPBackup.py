import os
import shutil
from datetime import datetime, date
from typing import Optional, Union

import discord
from discord.ext import commands

from SharkBot.Errors import ZIPBackup as Errors


def create_backup(dt: Optional[date] = None):
    if dt is None:
        dt = datetime.now().date()
    shutil.make_archive(f"data/live/backups/{dt}", "zip", "data/live/members")


def delete_backup(dt: Optional[date] = None):
    if dt is None:
        dt = datetime.now().date()
    if os.path.exists(f"data/live/backups/{dt}.zip"):
        os.remove(f"data/live/backups/{dt}.zip")
    else:
        raise Errors.BackupDoesNotExistError(f"{dt}.zip")


async def send_backup(channel: Union[discord.TextChannel, commands.Context], dt: Optional[date] = None):
    if dt is None:
        dt = datetime.now().date()
    if os.path.exists(f"data/live/backups/{dt}.zip"):
        with open(f"data/live/backups/{dt}.zip", "rb") as infile:
            file = discord.File(infile)
        await channel.send(f"Backup for {dt}", file=file)
    else:
        raise Errors.BackupDoesNotExistError(f"{dt}.zip")
