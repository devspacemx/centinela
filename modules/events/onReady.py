from bot import bot, config_migrated, migrated, prefix
from core import migration
from modules.tasks.loop import (check_cleanup_queued_guilds, cleandb,
                                maintain_presence, updates)
from modules.utils import database_updates, system_notification

print(__name__)

migrated = migration.migrate()
config_migrated = migration.migrateconfig()


@bot.event
async def on_ready():
    print("Centinela ready!")
    if migrated:
        await system_notification(
            None,
            "Your CSV files have been deleted and migrated to an SQLite"
            " `centinela.db` file.",
        )

    if config_migrated:
        await system_notification(
            None,
            "Your `config.ini` has been edited and your admin IDs are now stored in"
            f" the database.\nYou can add or remove them with `{prefix}admin` and"
            f" `{prefix}rm-admin`.",
        )

    await database_updates()
    maintain_presence.start()
    cleandb.start()
    check_cleanup_queued_guilds.start()
    updates.start()
