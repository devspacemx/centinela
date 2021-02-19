import configparser
import os

import discord

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

activities_file = "files/activities.csv"
activities = activity.Activities(activities_file)
db_file = "files/centinela.db"
db = database.Database(db_file)
