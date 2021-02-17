import discord
from bot import bot, db
from discord.ext import commands
from modules.utils import system_notification


@bot.command(name="adminlist")
@commands.has_permissions(administrator=True)
async def list_admin(ctx):
    # Lists all admin IDs in the database, mentioning them if possible
    admin_ids = db.get_admins(ctx.guild.id)

    if isinstance(admin_ids, Exception):
        await system_notification(
            ctx.message.guild.id,
            f"Database error when fetching admins:\n```\n{admin_ids}\n```",
        )
        return

    adminrole_objects = []
    for admin_id in admin_ids:
        adminrole_objects.append(discord.utils.get(
            ctx.guild.roles, id=admin_id).mention)

    if adminrole_objects:
        await ctx.send(
            "The bot admins on this server are:\n- "
            + "\n- ".join(adminrole_objects)
        )
    else:
        await ctx.send("There are no bot admins registered in this server.")