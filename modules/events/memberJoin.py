from common import db
from discord.ext import commands


class MemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        global db
        print('db')
        print(db)
        server_channel = db.fetch_welcomeChannel(member.guild.id)[0][0]
        # replace id with the welcome channel's id
        channel = self.bot.get_channel(server_channel)
        if channel is not None:
            await channel.send(f"¡Bienvenid@ **{member.name}** a la comunidad **DevSpace**! :wave:")
