from sys import exit as shutdown
from sys import platform

from discord.ext import commands
from modules.utils import restart


class Restart(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="restart")
    @commands.is_owner()
    async def restart_cmd(self, ctx):
        if platform != "win32":
            restart()
            await ctx.send("Restarting...")
            shutdown()  # sys.exit()

        else:
            await ctx.send("I cannot do this on Windows.")
