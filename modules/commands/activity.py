from bot import activities, bot, prefix
from discord.ext import commands

print(__name__)


@commands.is_owner()
@bot.command(name="activity")
async def add_activity(ctx):
    activity = ctx.message.content[(len(prefix) + len("activity")):].strip()
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
