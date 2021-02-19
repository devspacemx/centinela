from common import db
from discord.ext import commands
from modules.utils import isAdmin


class Notify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="notify")
    async def toggle_notify(self, ctx):
        if isAdmin(ctx.message.author, ctx.guild.id):
            notify = db.toggle_notify(ctx.guild.id)
            if notify:
                await ctx.send(
                    "Notifications have been set to **ON** for this server.\n"
                    "Use this command again to turn them off."
                )
            else:
                await ctx.send(
                    "Notifications have been set to **OFF** for this server.\n"
                    "Use this command again to turn them on."
                )
