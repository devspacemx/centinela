import discord
from bot import bot, db
from discord.ext import commands
from modules.utils import system_notification

print(__name__)


@bot.command(pass_context=True, name="admin")
@commands.has_permissions(administrator=True)
async def add_admin(ctx, role: discord.Role):
    # Adds an admin role ID to the database
    add = db.add_admin(role.id, ctx.guild.id)

    if isinstance(add, Exception):
        await system_notification(
            ctx.message.guild.id,
            f"Database error when adding a new admin:\n```\n{add}\n```",
        )
        return

    await ctx.send("Added the role to my admin list.")


@add_admin.error
async def add_admin_error(ctx, error):
    if isinstance(error, commands.RoleNotFound):
        await ctx.send("Please mention a valid @Role or role ID.")