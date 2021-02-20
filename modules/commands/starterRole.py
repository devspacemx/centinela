import discord
from common import db
from discord.ext import commands
from modules.utils import isAdmin, system_notification


class SetStarterRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="starterRole")
    @commands.has_permissions(administrator=True)
    async def setStarterRole(self, ctx, role: discord.Role):
        add = db.add_starterRole(ctx.guild.id, role.id)
        print('Role added: ', role.name)
        if isinstance(add, Exception):
            await system_notification(self.bot,
                                      ctx.message.guild.id,
                                      f"Database error when adding a new admin:\n```\n{add}\n```",
                                      )
            return
        await ctx.send(f"Role {role.name} set as starter role for new members")
