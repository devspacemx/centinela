
from bot import bot, db
from modules.utils import isAdmin


@bot.command(name="notify")
async def toggle_notify(ctx):
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
