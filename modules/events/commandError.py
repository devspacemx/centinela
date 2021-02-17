from asyncio import events

from bot import __version__, bot
from discord.ext import commands

print(__name__)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send("Only the bot owner may execute this command.")
