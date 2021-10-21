from __future__ import annotations

from datetime import datetime
from typing import List
import nextcord
from nextcord.embeds import Embed
from nextcord.message import Message
from pycoinmarketcap import CoinMarketCap
from currency_symbols import CurrencySymbols
import os

from db import add_crypto_def, get_def_cur, rem_crypto_def, get_crypto_def, set_def_cur

from pycoinmarketcap.errors import ErrorBadRequest


cm = CoinMarketCap(os.getenv("API_KEY"))

# round to 2 decimal places and format with comma spaces
def formatNum(f: float) -> str:
    return "{:,.2f}".format(f)


# use Client in order to manage custom commands
class BotClient(nextcord.Client):
    async def on_ready(self):
        print("Logged in as ", self.user)

    async def on_message(self, message: Message):
        # do not reply to self
        if message.author == self.user:
            return

        userid = str(message.author.id)

        cmd = message.content.split(" ", 1)
        command = cmd[0]

        # special commands
        if command == "p/add":
            async with message.channel.typing():
                try:
                    args = cmd[1]
                except Exception:
                    return await message.channel.send(
                        "Required some arguments for this command!"
                    )

                cryptos = [x.strip() for x in args.split(",")]
                add_crypto_def(userid, cryptos)

                return await message.channel.send(
                    f"Successfully added new cryptos to your defaults. [{','.join(cryptos)}]"
                )

        if command == "p/rem":
            async with message.channel.typing():
                try:
                    args = cmd[1]
                except Exception:
                    return await message.channel.send(
                        "Required some arguments for this command!"
                    )

                cryptos = [x.strip() for x in args.split(",")]
                rem_crypto_def(userid, cryptos)

                return await message.channel.send(
                    f"Successfully added new cryptos to your defaults. [{','.join(cryptos)}]"
                )

        if command == "p/setcurr":
            async with message.channel.typing():
                try:
                    args = cmd[1]
                except Exception:
                    return await message.channel.send(
                        "Required some arguments for this command!"
                    )

                set_def_cur(userid, args.strip())

                return await message.channel.send(
                    f"Successfully set default currency to {args.upper()}"
                )

        if command == "p/def":
            async with message.channel.typing():
                symbol = get_crypto_def(userid)
                currency = get_def_cur(userid)

                if len(symbol) == 0:
                    return await message.channel.send(
                        "No set default cryptocurrencies."
                    )

                await query_crypto_quote(message, symbol, currency)

        # if it doesn't start with prefix, return
        if not message.content.startswith("%"):
            return

        async with message.channel.typing():
            if message.content is None or len(message.content) < 3 or len(cmd) == 0:
                return await message.channel.send("Invalid Bot Command format!")

            symbol = command[1:]
            currency = "usd"

            if len(cmd) >= 2:
                currency = cmd[1]

                await query_crypto_quote(message, symbol, currency)


# get latest crypto quote and return embed
async def query_crypto_quote(message: Message, symbol: List[str] | str, currency: str):
    sym = symbol
    if not isinstance(symbol, str):
        sym = (",".join(symbol)).strip()

    try:
        q = cm.crypto_quotes_latest(symbol=sym, convert=currency, skip_invalid=True)
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
