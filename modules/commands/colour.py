import discord
from common import config, directory, prefix
from discord.ext import commands


class Colour(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="colour")
    async def set_colour(self, ctx):
        msg = ctx.message.content.split()
        args = len(msg) - 1
        if args:
            global botcolour
            colour = msg[1]
            try:
                botcolour = discord.Colour(int(colour, 16))

                config["server"]["colour"] = colour
                with open(f"{directory}/config.ini", "w") as configfile:
                    config.write(configfile)

                example = discord.Embed(
                    title="Example embed",
                    description="This embed has a new colour!",
                    colour=botcolour,
                )
                await ctx.send("Colour changed.", embed=example)

            except ValueError:
                await ctx.send(
                    "Please provide a valid hexadecimal value. Example:"
                    f" `{prefix}colour 0xffff00`"
                )

        else:
            await ctx.send(
                f"Please provide a hexadecimal value. Example: `{prefix}colour"
                " 0xffff00`"
            )
