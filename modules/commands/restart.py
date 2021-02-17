from sys import exit as shutdown
from sys import platform

from bot import bot
from discord.ext import commands
from modules.utils import restart


@commands.is_owner()
@bot.command(name="restart")
async def restart_cmd(ctx):
    if platform != "win32":
        restart()
        await ctx.send("Restarting...")
        shutdown()  # sys.exit()

    else:
        await ctx.send("I cannot do this on Windows.")
