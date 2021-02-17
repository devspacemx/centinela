from sys import exit as shutdown

from bot import bot
from discord.ext import commands


@commands.is_owner()
@bot.command(name="kill")
async def kill(ctx):
    await ctx.send("Shutting down...")
    shutdown()  # sys.exit()
