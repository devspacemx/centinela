from bot import __version__, bot
from core import github
from modules.utils import isAdmin


@bot.command(name="version")
async def print_version(ctx):
    if isAdmin(ctx.message.author, ctx.guild.id):
        latest = github.get_latest()
        await ctx.send(
            f"I am currently running Reaction Light v{__version__}. The latest"
            f" available version is v{latest}."
        )

    else:
        await ctx.send("You do not have an admin role.")
