import datetime

import discord
from common import __version__, activities, db, prefix
from core import migration
from discord.ext import commands, tasks
from discord.ext.commands.bot import Bot
from modules.utils import database_updates, system_notification

migrated = migration.migrate()
config_migrated = migration.migrateconfig()


class OnReady(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @tasks.loop(seconds=30)
    async def maintain_presence(self):
        # Loops through the activities specified in activities.csv
        activity = activities.get()
        game = discord.Game(activity)
        await self.bot.change_presence(status=discord.Status.online, activity=game)

    @tasks.loop(hours=24)
    async def cleandb(self):
        # Cleans the database by deleting rows of reaction role messages that don't exist anymore
        messages = db.fetch_all_messages()
        guilds = db.fetch_all_guilds()
        # Get the cleanup queued guilds
        cleanup_guild_ids = db.fetch_cleanup_guilds(guild_ids_only=True)

        if isinstance(messages, Exception):
            await system_notification(self.bot,
                                      None,
                                      "Database error when fetching messages during database"
                                      f" cleaning:\n```\n{messages}\n```",
                                      )
            return

        for message in messages:
            try:
                channel_id = message[1]
                channel = await self.bot.fetch_channel(channel_id)

                await channel.fetch_message(message[0])

            except discord.NotFound as e:
                # If unknown channel or unknown message
                if e.code == 10003 or e.code == 10008:
                    delete = db.delete(message[0], message[3])

                    if isinstance(delete, Exception):
                        await system_notification(self.bot,
                                                  channel.guild.id,
                                                  "Database error when deleting messages during database"
                                                  f" cleaning:\n```\n{delete}\n```",
                                                  )
                        return

                    await system_notification(self.bot,
                                              channel.guild.id,
                                              "I deleted the database entries of a message that was removed."
                                              f"\n\nID: {message} in {channel.mention}",
                                              )

            except discord.Forbidden:
                # If we can't fetch the channel due to the bot not being in the guild or permissions we usually cant mention it or get the guilds id using the channels object
                await system_notification(self.bot,
                                          message[3],
                                          "I do not have access to a message I have created anymore. "
                                          "I cannot manage the roles of users reacting to it."
                                          f"\n\nID: {message[0]} in channel {message[1]}",
                                          )

        if isinstance(guilds, Exception):
            await system_notification(self.bot,
                                      None,
                                      "Database error when fetching guilds during database"
                                      f" cleaning:\n```\n{guilds}\n```",
                                      )
            return

        for guild_id in guilds:
            try:
                await self.bot.fetch_guild(guild_id)
                if guild_id in cleanup_guild_ids:
                    db.remove_cleanup_guild(guild_id)

            except discord.Forbidden:
                # If unknown guild
                if guild_id in cleanup_guild_ids:
                    continue
                else:
                    db.add_cleanup_guild(guild_id, round(
                        datetime.datetime.utcnow().timestamp()))

        cleanup_guilds = db.fetch_cleanup_guilds()

        if isinstance(cleanup_guilds, Exception):
            await system_notification(self.bot,
                                      None,
                                      "Database error when fetching cleanup guilds during"
                                      f" cleaning:\n```\n{cleanup_guilds}\n```",
                                      )
            return

        current_timestamp = round(datetime.datetime.utcnow().timestamp())
        for guild in cleanup_guilds:
            if int(guild[1]) - current_timestamp <= -86400:
                # The guild has been invalid / unreachable for more than 24 hrs, try one more fetch then give up and purge the guilds database entries
                try:
                    await self.bot.fetch_guild(guild[0])
                    db.remove_cleanup_guild(guild[0])
                    continue

                except discord.Forbidden:
                    delete = db.remove_guild(guild[0])
                    delete2 = db.remove_cleanup_guild(guild[0])
                    if isinstance(delete, Exception):
                        await system_notification(self.bot,
                                                  None,
                                                  "Database error when deleting a guilds datebase entries during"
                                                  f" database cleaning:\n```\n{delete}\n```",
                                                  )
                        return

                    elif isinstance(delete2, Exception):
                        await system_notification(self.bot,
                                                  None,
                                                  "Database error when deleting a guilds datebase entries during"
                                                  f" database cleaning:\n```\n{delete2}\n```",
                                                  )
                        return

    @tasks.loop(hours=6)
    async def check_cleanup_queued_guilds(self):
        cleanup_guild_ids = db.fetch_cleanup_guilds(guild_ids_only=True)
        for guild_id in cleanup_guild_ids:
            try:
                await self.bot.fetch_guild(guild_id)
                db.remove_cleanup_guild(guild_id)

            except discord.Forbidden:
                continue

    @commands.Cog.listener()
    async def on_ready(self):
        print("Centinela ready!")
        if migrated:
            await system_notification(self.bot,
                                      None,
                                      "Your CSV files have been deleted and migrated to an SQLite"
                                      " `centinela.db` file.",
                                      )

        if config_migrated:
            await system_notification(self.bot,
                                      None,
                                      "Your `config.ini` has been edited and your admin IDs are now stored in"
                                      f" the database.\nYou can add or remove them with `{prefix}admin` and"
                                      f" `{prefix}rm-admin`.",
                                      )
        await database_updates(self.bot)
        self.maintain_presence.start()
        self.cleandb.start()
        self.check_cleanup_queued_guilds.start()
