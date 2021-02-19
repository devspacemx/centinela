from common import activities, prefix
from discord.ext import commands


class Activity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def activity(self, ctx):
        activity = ctx.message.content[(
            len(prefix) + len("activity")):].strip()
        if not activity:
            await ctx.send(
                "Please provide the activity you would like to"
                f" add.\n```\n{prefix}activity your activity text here\n```"
            )

        elif "," in activity:
            await ctx.send("Please do not use commas `,` in your activity.")

        else:
            activities.add(activity)
            await ctx.send(f"The activity `{activity}` was added succesfully.")
