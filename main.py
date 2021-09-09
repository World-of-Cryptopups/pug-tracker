from hata import Client, IntentFlag, Embed
from pycoingecko import CoinGeckoAPI
import os

bot = Client(
    os.getenv("TOKEN"),
    extensions="commands_v2",
    prefix=".",
    intents=IntentFlag(0).update_by_keys(guilds=True, guild_messages=True),
)
cg = CoinGeckoAPI()


@bot.events
async def ready(client):
    print(f"{client:f} logged in.")


@bot.commands
async def ping(ctx):
    await ctx.reply("Pong!")


@bot.commands
async def p(ctx, crypto: str = None, currency: str = "usd"):
    if crypto is None:
        await ctx.reply("No Currency to get.")
        return

    x = cg.get_price(
        ids=f"{crypto}",
        vs_currencies=f"{currency}",
        include_market_cap=True,
        include_24hr_vol=True,
        include_24hr_change=True,
        include_last_updated_at=True,
    )

    embed = Embed(f"{crypto.upper()} -> {currency.upper()}", "Current price").add_field(
        "Price", str(x[crypto][currency])
    )

    await ctx.reply(embed)


bot.start()
