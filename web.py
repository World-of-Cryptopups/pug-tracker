from threading import Thread
from flask import Flask
from main import BotClient

import os


app = Flask("")


@app.route("/")
def main():
    return "Your bot is running!"


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    server = Thread(target=run)
    server.start()


# run webapp
keep_alive()

# run bot
bot = BotClient()
bot.run(os.getenv("TOKEN"))
