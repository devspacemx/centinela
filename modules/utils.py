import os
from sys import platform

import discord
from common import __version__, db, db_file, directory, system_channel
from core import schema
from discord.ext.commands.bot import Bot


def isAdmin(member, guild_id):
    # Checks if command author has an admin role that was added with rl!admin
    admins = db.get_admins(guild_id)

    if isinstance(admins, Exception):
        print(f"Error when checking if the member is an admin:\n{admins}")
        return False

    try:
        member_roles = [role.id for role in member.roles]
        return [admin_role for admin_role in admins if admin_role in member_roles]

    except AttributeError:
        # Error raised from 'fake' users, such as webhooks
        return False


async def getChannel(bot: Bot, id):
    channel = bot.get_channel(id)

    if not channel:
        try:
            channel = await bot.fetch_channel(id)
        except discord.InvalidData:
            channel = None
        except discord.HTTPException:
            channel = None

    return channel


async def getGuild(bot: Bot, id):
    guild = bot.get_guild(id)

    if not guild:
        guild = await bot.fetch_guild(id)

    return guild


async def getUser(bot: Bot, id):
    user = bot.get_user(id)

    if not user:
        user = await bot.fetch_user(id)

    return user


def restart():
    # Create a new python process of bot.py and stops the current one
    os.chdir(directory)
    python = "python" if platform == "win32" else "python3"
    cmd = os.popen(f"nohup {python} bot.py &")
    cmd.close()


async def database_updates(bot: Bot):
    handler = schema.SchemaHandler(db_file, bot)
    if handler.version == 0:
        handler.zero_to_one()
        messages = db.fetch_all_messages()
        for message in messages:
            channel_id = message[1]
            channel = await getChannel(bot, channel_id)
            db.add_guild(channel.id, channel.guild.id)

    if handler.version == 1:
        handler.one_to_two()


async def system_notification(bot, guild_id, text):
    # Send a message to the system channel (if set)
    if guild_id:
        server_channel = db.fetch_systemchannel(guild_id)

        if isinstance(server_channel, Exception):
            await system_notification(bot,
                                      None,
                                      "Database error when fetching guild system"
                                      f" channels:\n```\n{server_channel}\n```\n\n{text}",
                                      )
            return

        if server_channel:
            server_channel = server_channel[0][0]

        if server_channel:
            try:
                target_channel = await getChannel(bot, server_channel)
                await target_channel.send(text)

            except discord.Forbidden:
                await system_notification(bot, None, text)

        else:
            await system_notification(bot, None, text)

    elif system_channel:
        try:
            target_channel = await getChannel(bot, system_channel)
            await target_channel.send(text)

        except discord.NotFound:
            print("I cannot find the system channel.")

        except discord.Forbidden:
            print("I cannot send messages to the system channel.")

    else:
        print(text)


async def formatted_channel_list(bot: Bot, channel):
    all_messages = db.fetch_messages(channel.id)
    if isinstance(all_messages, Exception):
        await system_notification(bot,
                                  channel.guild.id,
                                  f"Database error when fetching messages:\n```\n{all_messages}\n```",
                                  )
        return

    formatted_list = []
    counter = 1
    for msg_id in all_messages:
        try:
            old_msg = await channel.fetch_message(int(msg_id))

        except discord.NotFound:
            # Skipping reaction-role messages that might have been deleted without updating CSVs
            continue

        except discord.Forbidden:
            await system_notification(bot,
                                      channel.guild.id,
                                      "I do not have permissions to edit a reaction-role message"
                                      f" that I previously created.\n\nID: {msg_id} in"
                                      f" {channel.mention}",
                                      )
            continue

        entry = (
            f"`{counter}`"
            f" {old_msg.embeds[0].title if old_msg.embeds else old_msg.content}"
        )
        formatted_list.append(entry)
        counter += 1

    return formatted_list
