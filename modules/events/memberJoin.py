
from bot import __version__, bot, db

print(__name__)


@bot.event
async def on_member_join(member):
    server_channel = db.fetch_welcomeChannel(member.guild.id)[0][0]
    # replace id with the welcome channel's id
    channel = bot.get_channel(server_channel)
    await channel.send(f"¡Bienvenid@ **{member.name}** a la comunidad **DevSpace**! :wave:")
