from datetime import datetime
import nextcord
from nextcord.embeds import Embed
from nextcord.message import Message
from pycoinmarketcap import CoinMarketCap
from currency_symbols import CurrencySymbols
import os

from .web import keep_alive

from pycoinmarketcap.errors import ErrorBadRequest


cm = CoinMarketCap(os.getenv("API_KEY"))


def formatNum(f: float) -> str:
    return "{:,.2f}".format(f)


class BotClient(nextcord.Client):
    async def on_ready(self):
        print("Logged in as ", self.user)

    async def on_message(self, message: Message):
        if message.author == self.user:
            return

        if not message.content.startswith("%"):
            return

        async with message.channel.typing():
            rawMessage = message.content.split(" ")

            if (
                message.content is None
                or len(message.content) < 3
                or len(rawMessage) == 0
            ):
                return await message.channel.send("Invalid Bot Command format!")

            symbol = rawMessage[0][1:]
            currency = "usd"
            if len(rawMessage) >= 2:
                currency = rawMessage[1]

            try:
                q = cm.crypto_quotes_latest(
                    symbol=symbol, convert=currency, skip_invalid=True
                )
            except ErrorBadRequest as e:
                return await message.channel.send(e.error_message)

            for _, d in q.data.items():
                for c, x in d["quote"].items():
                    embed = (
                        Embed(
                            title=f"{d['symbol']} to {c}",
                            timestamp=datetime.now(),
                        )
                        .set_author(
                            name=d["name"],
                            url=f"https://coinmarketcap.com/currencies/{d['slug']}",
                            icon_url=f"https://s2.coinmarketcap.com/static/img/coins/128x128/{d['id']}.png",
                        )
                        .set_thumbnail(
                            url=f"https://s2.coinmarketcap.com/static/img/coins/128x128/{d['id']}.png"
                        )
                        .add_field(
                            name="Current Price",
                            value=f"{CurrencySymbols.get_symbol(c)} {formatNum(x['price'])}",
                        )
                        .add_field(
                            name="24h Volume",
                            value=f"{CurrencySymbols.get_symbol(c)} {formatNum(x['volume_24h'])}",
                        )
                        .add_field(
                            name="Market Cap",
                            value=f"{CurrencySymbols.get_symbol(c)} {formatNum(x['market_cap'])}",
                        )
                        .add_field(
                            name="1hr % Change",
                            value=f"{formatNum(x['percent_change_1h'])}%",
                        )
                        .add_field(
                            name="24h % Change",
                            value=f"{formatNum(x['percent_change_24h'])}%",
                        )
                        .add_field(
                            name="7d % Change",
                            value=f"{formatNum(x['percent_change_7d'])}%",
                        )
                        .set_footer(text="Pug Tracker | pycoinmarketcap - 2021")
                    )

                    await message.channel.send(embed=embed)


# run webapp
keep_alive()

# run bot
bot = BotClient()
bot.run(os.getenv("TOKEN"))
