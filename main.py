import nextcord
from nextcord.embeds import Embed
from nextcord.message import Message
from pycoinmarketcap import CoinMarketCap
import os

from pycoinmarketcap.errors import ErrorBadRequest


cm = CoinMarketCap(os.getenv("API_KEY"))


class BotClient(nextcord.Client):
    async def on_ready(self):
        print("Logged in as ", self.user)

    async def on_message(self, message: Message):
        if message.author == self.user:
            return

        if not message.content.startswith("%"):
            return

        rawMessage = message.content.split(" ")

        if message.content is None or len(message.content) < 3 or len(rawMessage) == 0:
            return await message.channel.send("Invalid Bot Command format!")

        symbol = rawMessage[0][1:]
        currency = rawMessage[1] if len(rawMessage) > 2 else "usd"

        try:
            q = cm.crypto_quotes_latest(symbol=symbol, convert=currency)
        except ErrorBadRequest as e:
            return await message.channel.send(e.error_message)

        for _, d in q.data.items():
            for c, x in d["quote"].items():
                embed = (
                    Embed(title=f"{d['symbol']} to {c}", description=d["name"])
                    .set_thumbnail(
                        url=f"https://s2.coinmarketcap.com/static/img/coins/128x128/{d['id']}.png"
                    )
                    .add_field(name="Current Price", value=str(x["price"]))
                    .add_field(name="24h Volume", value=str(x["volume_24h"]))
                    .set_footer(text="Pug Tracker | pycoinmarketcap - 2021")
                )

                await message.channel.send(embed=embed)


bot = BotClient()
bot.run(os.getenv("TOKEN"))
