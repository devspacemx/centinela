from common import __version__
from core import github
from discord.ext import commands
from modules.utils import isAdmin


class Version(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def version(self, ctx):
        if isAdmin(ctx.message.author, ctx.guild.id):
            latest = github.get_latest()
            await ctx.send(
                f"I am currently running Centinela v{__version__}"
            )
        else:
            await ctx.send("You do not have an admin role.")
