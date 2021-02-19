from common import __version__, botname, prefix
from discord.ext import commands
from modules.utils import isAdmin


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        if isAdmin(ctx.message.author, ctx.guild.id):
            await ctx.send(
                "**Reaction Role Messages**\n"
                f"- `{prefix}new` starts the creation process for a new"
                " reaction role message.\n"
                f"- `{prefix}edit` edits the text and embed of an existing reaction"
                " role message.\n"
                f"- `{prefix}reaction` adds or removes a reaction from an existing"
                " reaction role message.\n"
                f"- `{prefix}notify` toggles sending messages to users when they get/lose"
                " a role (default off) for the current server (the command affects only"
                " the server it was used in).\n"
                f"- `{prefix}colour` changes the colour of the embeds of new and newly"
                " edited reaction role messages.\n"
                "**Activities**\n"
                f"- `{prefix}activity` adds an activity for the bot to loop through and"
                " show as status.\n"
                f"- `{prefix}rm-activity` removes an activity from the bot's list.\n"
                f"- `{prefix}activitylist` lists the current activities used by the"
                " bot as statuses.\n"
            )
            await ctx.send(
                "**Admins**\n"
                f"- `{prefix}admin` adds the mentioned role to the list of {botname}"
                " admins, allowing them to create and edit reaction-role messages."
                " You need to be a server administrator to use this command.\n"
                f"- `{prefix}rm-admin` removes the mentioned role from the list of"
                f" {botname} admins, preventing them from creating and editing"
                " reaction-role messages. You need to be a server administrator to"
                " use this command.\n"
                f"- `{prefix}adminlist` lists the current admins on the server the"
                " command was run in by mentioning them and the current admins from"
                " other servers by printing out the role IDs. You need to be a server"
                " administrator to use this command.\n"
                "**System**\n"
                f"- `{prefix}systemchannel` updates the main or server system channel"
                " where the bot sends errors and update notifications.\n"
                "**Bot Control**\n"
                f"- `{prefix}kill` shuts down the bot.\n"
                f"- `{prefix}restart` restarts the bot. Only works on installations"
                " running on GNU/Linux.\n"
                f"- `{prefix}version` reports the bot's current version and the latest"
                " available one from GitHub.\n\n"
                f"{botname} is running version {__version__} of Centinela. You can"
                " find more resources, submit feedback, and report bugs at: "
                "<https://github.com/devspacemx/centinela>"
            )
        else:
            await ctx.send("You do not have an admin role.")
