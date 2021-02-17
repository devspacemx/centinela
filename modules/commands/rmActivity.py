from bot import activities, bot, commands, prefix


@commands.is_owner()
@bot.command(name="rm-activity")
async def remove_activity(ctx):
    activity = ctx.message.content[(len(prefix) + len("rm-activity")):].strip()
    if not activity:
        await ctx.send(
            "Please paste the activity you would like to"
            f" remove.\n```\n{prefix}rm-activity your activity text here\n```"
        )
        return

    removed = activities.remove(activity)
    if removed:
        await ctx.send(f"The activity `{activity}` was removed.")

    else:
        await ctx.send("The activity you mentioned does not exist.")
