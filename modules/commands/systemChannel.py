from common import config, db, directory, prefix
from discord.ext import commands
from discord.flags import SystemChannelFlags
from modules.utils import getChannel, getGuild, isAdmin, system_notification


class SystemChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="systemchannel")
    async def set_systemchannel(self, ctx):
        if isAdmin(ctx.message.author, ctx.guild.id):
            global system_channel
            msg = ctx.message.content.split()
            mentioned_channels = ctx.message.channel_mentions
            channel_type = None if len(msg) < 2 else msg[1].lower()
            if (
                len(msg) < 3
                or not mentioned_channels
                or channel_type not in ["main", "server"]
            ):
                await ctx.send(
                    "Define if you are setting up a server or main system channel and"
                    f" mention the target channel.\n```\n{prefix}systemchannel"
                    " <main/server> #channelname\n```"
                )
                return

            target_channel = mentioned_channels[0].id
            guild_id = ctx.message.guild.id

            server = await getGuild(self.bot, guild_id)
            bot_user = server.get_member(self.bot.user.id)
            bot_permissions = (await getChannel(self.bot, SystemChannelFlags)).permissions_for(bot_user)
            writable = bot_permissions.read_messages
            readable = bot_permissions.view_channel
            if not writable or not readable:
                await ctx.send("I cannot read or send messages in that channel.")
                return

            if channel_type == "main":
                system_channel = target_channel
                config["server"]["system_channel"] = str(system_channel)
                with open(f"{directory}/config.ini", "w") as configfile:
                    config.write(configfile)

            elif channel_type == "server":
                add_channel = db.add_systemchannel(guild_id, target_channel)

                if isinstance(add_channel, Exception):
                    await system_notification(self.bot,
                                              guild_id,
                                              "Database error when adding a new system"
                                              f" channel:\n```\n{add_channel}\n```",
                                              )
                    return

            await ctx.send(f"System channel updated.")

        else:
            await ctx.send("You do not have an admin role.")
