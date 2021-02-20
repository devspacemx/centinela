from discord.ext.commands.bot import Bot

from .activity import *
from .activityList import *
from .admin import *
from .adminList import *
from .colour import *
from .edit import *
from .help import *
from .kill import *
from .new import *
from .notify import *
from .reaction import *
from .removeAdmin import *
from .restart import *
from .rmActivity import *
from .starterRole import *
from .systemChannel import *
from .version import *
from .welcomeChannel import *


def init(bot: Bot):
    bot.add_cog(Help(bot))
    bot.add_cog(Version(bot))
    bot.add_cog(Activity(bot))
    bot.add_cog(WelcomeChannel(bot))
    bot.add_cog(AdminList(bot))
    bot.add_cog(ActivityList(bot))
    bot.add_cog(AddAdmin(bot))
    bot.add_cog(Colour(bot))
    bot.add_cog(Kill(bot))
    bot.add_cog(SystemChannel(bot))
    bot.add_cog(New(bot))
    bot.add_cog(Notify(bot))
    bot.add_cog(Edit(bot))
    bot.add_cog(Reaction(bot))
    bot.add_cog(RemoveAdmin(bot))
    bot.add_cog(Restart(bot))
    bot.add_cog(RemoveActivity(bot))
    bot.add_cog(SetStarterRole(bot))
