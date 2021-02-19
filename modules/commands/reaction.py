import discord
from common import config, db, directory, prefix
from discord.ext import commands
from discord.flags import SystemChannelFlags
from modules.utils import formatted_channel_list, isAdmin, system_notification


class Reaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reaction")
    async def edit_reaction(self, ctx):
        if isAdmin(ctx.message.author, ctx.guild.id):
            msg_values = ctx.message.content.split()
            mentioned_roles = ctx.message.role_mentions
            mentioned_channels = ctx.message.channel_mentions
            if len(msg_values) < 4:
                if not mentioned_channels:
                    await ctx.send(
                        f" To get started, type:\n```\n{prefix}reaction add"
                        f" #channelname\n```or\n```\n{prefix}reaction remove"
                        " #channelname\n```"
                    )
                    return

                channel = ctx.message.channel_mentions[0]
                all_messages = await formatted_channel_list(self.bot, channel)
                if len(all_messages) == 1:
                    await ctx.send(
                        "There is only one reaction-role messages in this channel."
                        f" **Type**:\n```\n{prefix}reaction add #{channel.name} 1"
                        f" :reaction: @rolename\n```or\n```\n{prefix}reaction remove"
                        f" #{channel.name} 1 :reaction:\n```"
                    )
                    return

                elif len(all_messages) > 1:
                    await ctx.send(
                        f"There are **{len(all_messages)}** reaction-role messages in this"
                        f" channel. **Type**:\n```\n{prefix}reaction add #{channel.name}"
                        " MESSAGE_NUMBER :reaction:"
                        f" @rolename\n```or\n```\n{prefix}reaction remove"
                        f" #{channel.name} MESSAGE_NUMBER :reaction:\n```\nThe list of the"
                        " current reaction-role messages is:\n\n"
                        + "\n".join(all_messages)
                    )
                    return

                else:
                    await ctx.send("There are no reaction-role messages in that channel.")
                    return

            action = msg_values[1].lower()
            channel = ctx.message.channel_mentions[0]
            message_number = msg_values[3]
            reaction = msg_values[4]
            if action == "add":
                if mentioned_roles:
                    role = mentioned_roles[0]
                else:
                    await ctx.send("You need to mention a role to attach to the reaction.")
                    return

            all_messages = db.fetch_messages(channel.id)
            if isinstance(all_messages, Exception):
                await system_notification(self.bot,
                                          ctx.message.guild.id,
                                          f"Database error when fetching messages:\n```\n{all_messages}\n```",
                                          )
                return

            counter = 1
            if all_messages:
                message_to_edit_id = None
                for msg_id in all_messages:
                    # Loop through all msg_ids and stops when the counter matches the user input
                    if str(counter) == message_number:
                        message_to_edit_id = msg_id
                        break

                    counter += 1

            else:
                await ctx.send("You selected a reaction-role message that does not exist.")
                return

            if message_to_edit_id:
                message_to_edit = await channel.fetch_message(int(message_to_edit_id))

            else:
                await ctx.send(
                    "Select a valid reaction-role message number (i.e. the number"
                    " to the left of the reaction-role message content in the list"
                    " above)."
                )
                return

            if action == "add":
                try:
                    # Check that the bot can actually use the emoji
                    await message_to_edit.add_reaction(reaction)

                except discord.HTTPException:
                    await ctx.send(
                        "You can only use reactions uploaded to servers the bot has access"
                        " to or standard emojis."
                    )
                    return

                react = db.add_reaction(message_to_edit.id, role.id, reaction)
                if isinstance(react, Exception):
                    await system_notification(self.bot,
                                              ctx.message.guild.id,
                                              "Database error when adding a reaction to a message in"
                                              f" {message_to_edit.channel.mention}:\n```\n{react}\n```",
                                              )
                    return

                if not react:
                    await ctx.send("That message already has a reaction-role combination with"
                                   " that reaction.")
                    return

                await ctx.send("Reaction added.")

            elif action == "remove":
                try:
                    await message_to_edit.clear_reaction(reaction)

                except discord.HTTPException:
                    await ctx.send("Invalid reaction.")
                    return

                react = db.remove_reaction(message_to_edit.id, reaction)
                if isinstance(react, Exception):
                    await system_notification(self.bot,
                                              ctx.message.guild.id,
                                              "Database error when adding a reaction to a message in"
                                              f" {message_to_edit.channel.mention}:\n```\n{react}\n```",
                                              )
                    return

                await ctx.send("Reaction removed.")

        else:
            await ctx.send("You do not have an admin role.")
