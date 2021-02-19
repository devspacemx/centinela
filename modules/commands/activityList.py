from common import activities
from core.activity import Activities
from discord.ext import commands


class ActivityList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="activitylist")
    @commands.is_owner()
    async def activityList(self, ctx):
        formatted_list = []
        for activity in activities.activity_list:
            formatted_list.append(f"`{activity}`")
        await ctx.send(
            "The current activities are:\n- " + "\n- ".join(formatted_list)
        )
