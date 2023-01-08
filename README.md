# SharkBot 
> Developed by [James Donald](https://jdonald.co.uk)

SharkBot is a Discord Bot I am developing for my Clan's Discord Server. 
Originally created to monitor and tally up our clan's count-to-6969 channel, he became a much greater project for me, a space to test out new ideas and learn to use the discord.py API
## Dependencies
These need to be installed prior to running SharkBot. These can be found in [`requirements.txt`](requirements.txt).
Run `pip install -r requirements.txt` to install them.
> [`discord.py`](https://pypi.org/project/discord.py/)
> [`firebase_admin`](https://pypi.org/project/firebase_admin/)
> [`psutil`](https://pypi.org/project/psutil/)
> [`humanize`](https://pypi.org/project/humanize/)
>[`colorama`](https://pypi.org/project/colorama/)
## Cogs
In more recent versions of SharkBot I have begun using Cogs in order to keep different categories of command contained in separate files, as well as making updates easier. Where I used to have to reboot the whole pi to apply an update, I can now just upload the new code, and tell SharkBot to pull the latest commit and just reboot the Cogs I want to update.
- [Admin](cogs/admin.py) - Commands for admin purposes, such as purging messages or raising `TestError` during production
-  [Core](cogs/core.py) - Core commands that don't really have a place in other Cogs
-  [Count](cogs/count.py) - Commands and listeners related to the `count` tracking and rewards
-  [Database](cogs/database.py) - Commands for `Firestore` and the data uploading loop
-  [Destiny](cogs/destiny.py) - Commands related to Destiny 2
-  [Economy](cogs/economy.py) - Commands related to the in-game currency
-  [Errors](cogs/errors.py) - The Error Handling process
-  [Fun](cogs/fun.py) - Commands purely for fun, such as `$coinflip` and the Birthday Checking loop
-  [Icon](cogs/icon.py) - Commands and listeners so SharkBot keeps track of the icons it can use
-  [Items](cogs/items.py) - Commands related to the items and collections, such as `$inventory` and `$collection`
-  [Item Admin](cogs/itemadmin.py) - Items had so many commands, I moved the ones with admin permissions into their own Cog
-  [Levels](cogs/levels.py) - Commands related to the xp and levels system
-  [Lootbox](cogs/lootbox.py) - Commands related to the lootboxes, such as `$claim` and `$open`
-  [Missions](cogs/missions.py) - Commands related to Members' Missions
-  [Redeem](cogs/redeem.py) - `$redeem` to redeem promo codes, and notify dev when this is done
-  [Shop](cogs/shop.py) - Commands related to buying items, such as `$shop` and `$buy`
-  [Stats](cogs/stats.py) - Commands related to the stat trackers for Members
-  [Test](cogs/test.py) - Commands and methods used during testing
-  [Vault](cogs/vault.py) - Commands related to the Members' storage vaults, a way to store items away from your inventory so they don't accidentally get opened or sold
-  [Voice](cogs/voice.py) - Commands related to voice channels
-  [Zip Backup](cogs/zipbackup.py) - Loop to send a `.zip` folder containing a backup of member data every day

## Thanks
HxRL and LxKE have been consistent supporters in the production of this bot. They are two friends of mine; HxRL worked on a project for Valorant Commands that never came to fruition, and LxKE comes up with the ideas for most of the items
