import discord
from common import botcolour, botname, db, logo, prefix
from discord.ext import commands
from modules.utils import (formatted_channel_list, getChannel, isAdmin,
                           system_notification)


class Edit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="edit")
    async def edit_selector(self, ctx):
        if isAdmin(ctx.message.author, ctx.guild.id):
            # Reminds user of formatting if it is wrong
            msg_values = ctx.message.content.split()
            if len(msg_values) < 2:
                await ctx.send(
                    f"**Type** `{prefix}edit #channelname` to get started. Replace"
                    " `#channelname` with the channel where the reaction-role message you"
                    " wish to edit is located."
                )
                return

            elif len(msg_values) == 2:
                try:
                    channel_id = ctx.message.channel_mentions[0].id

                except IndexError:
                    await ctx.send("You need to mention a channel.")
                    return

                channel = await getChannel(self.bot, channel_id)
                all_messages = await formatted_channel_list(self.bot, channel)
                if len(all_messages) == 1:
                    await ctx.send(
                        "There is only one reaction-role message in this channel."
                        f" **Type**:\n```\n{prefix}edit #{channel.name} // 1 // New Message"
                        " // New Embed Title (Optional) // New Embed Description"
                        " (Optional)\n```\nto edit the reaction-role message. You can type"
                        " `none` in any of the argument fields above (e.g. `New Message`)"
                        " to make the bot ignore it."
                    )

                elif len(all_messages) > 1:
                    await ctx.send(
                        f"There are **{len(all_messages)}** reaction-role messages in this"
                        f" channel. **Type**:\n```\n{prefix}edit #{channel.name} //"
                        " MESSAGE_NUMBER // New Message // New Embed Title (Optional) //"
                        " New Embed Description (Optional)\n```\nto edit the desired one."
                        " You can type `none` in any of the argument fields above (e.g."
                        " `New Message`) to make the bot ignore it. The list of the"
                        " current reaction-role messages is:\n\n"
                        + "\n".join(all_messages)
                    )

                else:
                    await ctx.send("There are no reaction-role messages in that channel.")

            elif len(msg_values) > 2:
                try:
                    # Tries to edit the reaction-role message
                    # Raises errors if the channel sent was invalid or if the bot cannot edit the message
                    channel_id = ctx.message.channel_mentions[0].id
                    channel = await getChannel(self.bot, channel_id)
                    msg_values = ctx.message.content.split(" // ")
                    selector_msg_number = msg_values[1]
                    all_messages = db.fetch_messages(channel_id)

                    if isinstance(all_messages, Exception):
                        await system_notification(self.bot,
                                                  ctx.message.guild.id,
                                                  "Database error when fetching"
                                                  f" messages:\n```\n{all_messages}\n```",
                                                  )
                        return

                    counter = 1
                    if all_messages:
                        message_to_edit_id = None
                        for msg_id in all_messages:
                            # Loop through all msg_ids and stops when the counter matches the user input
                            if str(counter) == selector_msg_number:
                                message_to_edit_id = msg_id
                                break

                            counter += 1

                    else:
                        await ctx.send(
                            "You selected a reaction-role message that does not exist."
                        )
                        return

                    if message_to_edit_id:
                        old_msg = await channel.fetch_message(int(message_to_edit_id))

                    else:
                        await ctx.send(
                            "Select a valid reaction-role message number (i.e. the number"
                            " to the left of the reaction-role message content in the list"
                            " above)."
                        )
                        return
                    await old_msg.edit(suppress=False)
                    selector_msg_new_body = (
                        msg_values[2] if msg_values[2].lower(
                        ) != "none" else None
                    )
                    selector_embed = discord.Embed()

                    if len(msg_values) > 3 and msg_values[3].lower() != "none":
                        selector_embed.title = msg_values[3]
                        selector_embed.colour = botcolour
                        selector_embed.set_footer(
                            text=f"{botname}", icon_url=logo)

                    if len(msg_values) > 4 and msg_values[4].lower() != "none":
                        selector_embed.description = msg_values[4]
                        selector_embed.colour = botcolour
                        selector_embed.set_footer(
                            text=f"{botname}", icon_url=logo)

                    try:
                        if selector_embed.title or selector_embed.description:
                            await old_msg.edit(
                                content=selector_msg_new_body, embed=selector_embed
                            )

                        else:
                            await old_msg.edit(content=selector_msg_new_body, embed=None)

                        await ctx.send("Message edited.")
                    except discord.Forbidden:
                        await ctx.send("I can only edit messages that are created by me, please edit the message in some other way.")
                        return
                    except discord.HTTPException as e:
                        if e.code == 50006:
                            await ctx.send(
                                "You can't use an empty message as role-reaction message."
                            )

                        else:
                            guild_id = ctx.message.guild.id
                            await system_notification(self.bot, guild_id, str(e))

                except IndexError:
                    await ctx.send("The channel you mentioned is invalid.")

                except discord.Forbidden:
                    await ctx.send("I do not have permissions to edit the message.")

        else:
            await ctx.send("You do not have an admin role.")
