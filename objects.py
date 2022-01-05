import discord
import secret
from builtins import bot

if secret.testBot:
    import testids as ids
else:
    import ids

async def fetch_all():
    server = await bot.fetch_guild(ids.server)
    
    roles = {}
    for role in ids.roles:
        roles[role] = server.get_role(ids.roles[role])

    users = {}
    for user in ids.users:
        users[user] = await bot.fetch_user(ids.users[user])

    channels = {}
    for channel in ids.channels:
        channels[channel] = await bot.fetch_channel(ids.channels[channel])

    return server, roles, users, channels

server, roles, users, channels = fetch_all()

blacklist = [users["MEE6"]]

mods = [users["Chaos"], users["Luke"], users["HxRL"]]



