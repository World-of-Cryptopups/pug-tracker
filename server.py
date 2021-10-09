from main import BotClient
import os

# run bot
bot = BotClient()
bot.run(os.getenv("TOKEN"))
