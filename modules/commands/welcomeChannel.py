
from bot import bot, db
from modules.utils import isAdmin, system_notification


@bot.command(name="welcomechannel")
async def set_welcomechannel(ctx):
    if isAdmin(ctx.message.author, ctx.guild.id):
        mentioned_channels = ctx.message.channel_mentions
        target_channel = mentioned_channels[0].id
        guild_id = ctx.message.guild.id
        add_channel = db.add_welcomeChannel(guild_id, target_channel)
        if isinstance(add_channel, Exception):
            await system_notification(
                guild_id,
                "Database error when adding a new system"
                f" channel:\n```\n{add_channel}\n```",
            )
            return
        await ctx.send(f"Welcome channel updated.")

    else:
        await ctx.send("You do not have an admin role.")
