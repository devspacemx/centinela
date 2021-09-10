import discord
from common import db
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.guild import Guild
from discord.utils import get


class MemberJoin(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        server_channel = db.fetch_welcomeChannel(member.guild.id)[0]
        starter_role_id = db.fetch_starterRole(member.guild.id)[0]
        channel = self.bot.get_channel(server_channel)
        role = discord.utils.get(member.guild.roles, id=starter_role_id)
        if role is not None:
            await member.add_roles(role)
        if channel is not None:
            await channel.send(f"¡Te damos la bienvenida! **@{member.name}** a la comunidad **DevSpace** :wave:")
