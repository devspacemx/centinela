from bot import activities, bot
from core.activity import Activities
from discord.ext import commands

print(__name__)


@commands.is_owner()
@bot.command(name="activitylist")
async def list_activities(ctx):
    if Activities.activity_list:
        formatted_list = []
        for activity in activities.activity_list:
            formatted_list.append(f"`{activity}`")

        await ctx.send(
            "The current activities are:\n- " + "\n- ".join(formatted_list)
        )

    else:
        await ctx.send("There are no activities to show.")
