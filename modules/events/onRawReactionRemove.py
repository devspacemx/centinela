import discord
from common import db
from discord.ext import commands
from modules.utils import getGuild, system_notification


class OnRawReactionRemove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        reaction = str(payload.emoji)
        msg_id = payload.message_id
        user_id = payload.user_id
        guild_id = payload.guild_id
        exists = db.exists(msg_id)

        if isinstance(exists, Exception):
            await system_notification(self.bot,
                                      guild_id,
                                      f"Database error after a user removed a reaction:\n```\n{exists}\n```",
                                      )

        elif exists:
            # Checks that the message that was unreacted to is a reaction-role message managed by the bot
            reactions = db.get_reactions(msg_id)

            if isinstance(reactions, Exception):
                await system_notification(self.bot,
                                          guild_id,
                                          f"Database error when getting reactions:\n```\n{reactions}\n```",
                                          )

            elif reaction in reactions:
                role_id = reactions[reaction]
                # Removes role if it has permissions, else 403 error is raised
                server = await getGuild(self.bot, guild_id)
                member = server.get_member(user_id)

                if not member:
                    member = await server.fetch_member(user_id)

                role = discord.utils.get(server.roles, id=role_id)
                try:
                    await member.remove_roles(role)
                    if db.notify(guild_id):
                        await member.send(f"You do not have the following role anymore: **{role.name}**")

                except discord.Forbidden:
                    await system_notification(self.bot,
                                              guild_id,
                                              "Someone tried to remove a role from themselves but I do not have"
                                              " permissions to remove it. Ensure that I have a role that is"
                                              " hierarchically higher than the role I have to remove, and that I"
                                              " have the `Manage Roles` permission.",
                                              )
