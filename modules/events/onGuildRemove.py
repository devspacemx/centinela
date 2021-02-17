from bot import bot, db


@bot.event
async def on_guild_remove(guild):
    db.remove_guild(guild.id)
