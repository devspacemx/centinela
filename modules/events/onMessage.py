from bot import bot

print(__name__)


@bot.event
async def on_message(message):
    await bot.process_commands(message)
