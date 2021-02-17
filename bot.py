"""
MIT License

Copyright (c) 2019-2021 eibex

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import configparser
import importlib
import os

import discord
from discord.ext import commands

from core import activity, database

directory = os.path.dirname(os.path.realpath(__file__))
with open(f"{directory}/.version") as f:
    __version__ = f.read().rstrip("\n").rstrip("\r")

folder = f"{directory}/files"
config = configparser.ConfigParser()
config.read(f"{directory}/config.ini")
logo = str(config.get("server", "logo"))
TOKEN = str(config.get("server", "token"))
botname = str(config.get("server", "name"))
prefix = str(config.get("server", "prefix"))
botcolour = discord.Colour(int(config.get("server", "colour"), 16))
system_channel = (
    int(config.get("server", "system_channel"))
    if config.get("server", "system_channel")
    else None
)

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.messages = True
intents.emojis = True

bot = commands.Bot(command_prefix=prefix, intents=intents)

bot.remove_command("help")

activities_file = f"{directory}/files/activities.csv"
activities = activity.Activities(activities_file)
db_file = f"{directory}/files/centinela.db"
db = database.Database(db_file)
# Run bot only when invoked directly
if __name__ == "__main__":
    try:
        botEvents = importlib.import_module('modules.events')
        # botCommands = importlib.import_module('modules.commands')
        # botTasks = importlib.import_module('modules.tasks')
        bot.run(TOKEN)
    except discord.PrivilegedIntentsRequired:
        print("[Login Failure] You need to enable the server members intent on the Discord Developers Portal.")

    except discord.errors.LoginFailure:
        print("[Login Failure] The token inserted in config.ini is invalid.")
