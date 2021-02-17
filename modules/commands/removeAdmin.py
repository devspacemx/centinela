import discord
from bot import bot, db
from discord.ext import commands
from modules.utils import system_notification


@bot.command(name="rm-admin")
@commands.has_permissions(administrator=True)
async def remove_admin(ctx, role: discord.Role):
    # Removes an admin role ID from the database
    remove = db.remove_admin(role.id, ctx.guild.id)

    if isinstance(remove, Exception):
        await system_notification(
            ctx.message.guild.id,
            f"Database error when removing an admin:\n```\n{remove}\n```",
        )
        return

    await ctx.send("Removed the role from my admin list.")


@remove_admin.error
async def remove_admin_error(ctx, error):
    if isinstance(error, commands.RoleNotFound):
        await ctx.send("Please mention a valid @Role or role ID.")
