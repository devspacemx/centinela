import importlib

import discord
from discord.ext import commands

from common import TOKEN, intents, prefix

bot = commands.Bot(command_prefix=prefix, intents=intents)

bot.remove_command("help")

# Run bot only when invoked directly
if __name__ == "__main__":
    try:
        print('Starting...')
        botCommands = importlib.import_module('modules.commands')
        botCommands.init(bot)
        botEvents = importlib.import_module('modules.events')
        botEvents.init(bot)
        bot.run(TOKEN)
    except discord.PrivilegedIntentsRequired:
        print("[Login Failure] You need to enable the server members intent on the Discord Developers Portal.")

    except discord.errors.LoginFailure:
        print("[Login Failure] The token inserted in config.ini is invalid.")
