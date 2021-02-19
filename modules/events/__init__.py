from discord.ext.commands.bot import Bot

from .commandError import *
from .memberJoin import *
from .onGuildRemove import *
from .onRawReactionAdd import *
from .onRawReactionRemove import *
from .onReady import *


def init(bot: Bot):
    bot.add_cog(MemberJoin(bot))
    bot.add_cog(OnReady(bot))
    bot.add_cog(CommandError(bot))
    bot.add_cog(OnGuildRemove(bot))
    bot.add_cog(OnRawReactionAdd(bot))
    bot.add_cog(OnRawReactionRemove(bot))
