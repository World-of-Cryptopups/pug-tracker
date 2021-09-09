from hata import Client, IntentFlag, Message
import os

bot = Client(
    os.getenv("TOKEN"),
    extensions="commands",
    prefix=".",
    intents=IntentFlag(0).update_by_keys(guilds=True, guild_messages=True),
)


@bot.events
async def ready(client):
    print(f"{client:f} logged in.")


@bot.commands
async def ping(client, message):
    return "pong"


bot.start()
