# SharkBot
SharkBot is a Discord Bot I am developing for my Clan's Discord Server. 
Originally created to monitor and tally up our clan's count-to-6969 channel, he became a much greater project for me, a space to test out new ideas and learn to use the discord.py API
## Cogs
In more recent versions of SharkBot I have begun using Cogs in order to keep different categories of command contained in separate files, as well as making updates easier. Where I used to have to reboot the whole pi to apply an update, I can now just upload the new code, and tell SharkBot to pull the latest commit and just reboot the Cogs I want to update.
### [Core](https://github.com/ChaosCantrip/SharkBot/blob/main/cogs/core.py)
This cog is used to house the core commands of SharkBot, that don't really fit into a category.
### [Count](https://github.com/ChaosCantrip/SharkBot/blob/main/cogs/count.py)
This cog is used to house any commands relating to our clan's ongoing counting challenge.
### [Economy](https://github.com/ChaosCantrip/SharkBot/blob/main/cogs/economy.py)
This cog is used to house any commands relating to the Shark Tokens economy. This isn't really used in the server, and was just more for my own entertainment and to see if I could implement it.
### [Generators](https://github.com/ChaosCantrip/SharkBot/blob/main/cogs/generators.py)
This cog is used to house any commands that generate a random result, such as a coin flip or dice roll.
### [Errors](https://github.com/ChaosCantrip/SharkBot/blob/main/cogs/errors.py)
This cog is used to house the error handling system, so I could alter it without rebooting the whole pi, as it was originally held in the main.py
### [Valorant](https://github.com/ChaosCantrip/SharkBot/blob/main/cogs/valorant.py)
This cog is used to house the commands related to Hxrl's Valorant Analysis.
