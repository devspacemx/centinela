import discord
from bot import bot, db
from modules.utils import getchannel, getguild, getuser, system_notification


@bot.event
async def on_raw_reaction_add(payload):
    reaction = str(payload.emoji)
    msg_id = payload.message_id
    ch_id = payload.channel_id
    user_id = payload.user_id
    guild_id = payload.guild_id
    exists = db.exists(msg_id)

    if isinstance(exists, Exception):
        await system_notification(
            guild_id,
            f"Database error after a user added a reaction:\n```\n{exists}\n```",
        )

    elif exists:
        # Checks that the message that was reacted to is a reaction-role message managed by the bot
        reactions = db.get_reactions(msg_id)

        if isinstance(reactions, Exception):
            await system_notification(
                guild_id,
                f"Database error when getting reactions:\n```\n{reactions}\n```",
            )
            return

        ch = await getchannel(ch_id)
        msg = await ch.fetch_message(msg_id)
        user = await getuser(user_id)
        if reaction not in reactions:
            # Removes reactions added to the reaction-role message that are not connected to any role
            await msg.remove_reaction(reaction, user)

        else:
            # Gives role if it has permissions, else 403 error is raised
            role_id = reactions[reaction]
            server = await getguild(guild_id)
            member = server.get_member(user_id)
            role = discord.utils.get(server.roles, id=role_id)
            if user_id != bot.user.id:
                try:
                    await member.add_roles(role)
                    if db.notify(guild_id):
                        await user.send(f"You now have the following role: **{role.name}**")

                except discord.Forbidden:
                    await system_notification(
                        guild_id,
                        "Someone tried to add a role to themselves but I do not have"
                        " permissions to add it. Ensure that I have a role that is"
                        " hierarchically higher than the role I have to assign, and"
                        " that I have the `Manage Roles` permission.",
                    )