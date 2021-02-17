
import os
from shutil import copy
from sys import exit as shutdown
from sys import platform

from bot import bot, db_file, directory
from discord.ext import commands
from modules.utils import restart


@commands.is_owner()
@bot.command(name="update")
async def update(ctx):
    if platform != "win32":
        await ctx.send("Attempting update...")
        os.chdir(directory)
        cmd = os.popen("git fetch")
        cmd.close()
        cmd = os.popen("git pull")
        cmd.close()
        await ctx.send("Creating database backup...")
        copy(db_file, f"{db_file}.bak")
        restart()
        await ctx.send("Restarting...")
        shutdown()  # sys.exit()

    else:
        await ctx.send("I cannot do this on Windows.")
