from sys import exit as shutdown

from discord.ext import commands


class Kill(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kill")
    @commands.is_owner()
    async def kill(self, ctx):
        await ctx.send("Shutting down...")
        shutdown()  # sys.exit()
