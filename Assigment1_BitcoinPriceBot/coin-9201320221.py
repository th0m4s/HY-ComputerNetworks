# coin-9201320221.py
# ENE0419 - Computer Networks - Assignment 1 - Bitcoin price bot
# Thomas LEDOS - https://github.com/th0m4s/HY-ComputerNetworks

import os
import requests
import schedule
import telepot
import time

from dotenv import load_dotenv
from telepot.loop import MessageLoop

DATA_URL = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR,KRW"

load_dotenv()
destination_id = -1
old_data = None

try:
    if os.path.exists("destination_id.txt"):
        with open("destination_id.txt", "r") as file:
            destination_id = file.read()
            destination_id = int(destination_id)
except PermissionError:
    print("Cannot read current destination id, please send the start command again!")


def get_data():
    response = requests.get(DATA_URL)
    if response.status_code != 200:
        print("Cannot get prices from cryptocompare.com")
        print(response.status_code, response.text)
        return

    data = response.json()
    return {
        "USD": round(data["USD"], 2),
        "EUR": round(data["EUR"], 2),
        "KRW": int(data["KRW"])
    }


def send_prices():
    global old_data
    if destination_id < 0:
        return

    data = get_data()
    if data is None:
        bot.sendMessage(destination_id, "Oops, it looks like I cannot get the prices ;(")
        return

    message = "🏦 Current prices:"
    message += "\n ₿1 = ${:,} ".format(data["USD"])
    if old_data is not None and old_data["USD"] != data["USD"]:
        message += ("(up ${:,})" if data["USD"] > old_data["USD"] else
                    "(down ${:,})").format(abs(round(data["USD"] - old_data["USD"], 2)))
    message += "\n ₿1 = €{:,} ".format(data["EUR"])
    if old_data is not None and old_data["EUR"] != data["EUR"]:
        message += ("(up €{:,})" if data["EUR"] > old_data["EUR"] else
                    "(down €{:,})").format(abs(round(data["EUR"] - old_data["EUR"], 2)))
    message += "\n ₿1 = ₩{:,} ".format(data["KRW"])
    if old_data is not None and old_data["KRW"] != data["KRW"]:
        message += ("(up ₩{:,})" if data["KRW"] > old_data["KRW"] else
                    "(down ₩{:,})").format(abs(int(data["KRW"] - old_data["KRW"])))

    bot.sendMessage(destination_id, message)
    old_data = data


def handle_bot_message(message):
    global destination_id
    content_type, chat_type, chat_id = telepot.glance(message)
    if content_type == "text":
        contents = message["text"]
        if contents == "/start":
            destination_id = chat_id
            bot.sendMessage(chat_id, "Hi, thanks for using me, you'll now receive my updates!")

            try:
                with open("destination_id.txt", "w") as file:
                    file.write(str(destination_id))
            except PermissionError:
                print("Cannot write current destination id, use will have to send the /start \
                    command again!")
                bot.sendMessage(chat_id, "I cannot save your account, you'll have to send the \
                    /start command again after I'll restart.")
        elif contents == "/stop":
            if chat_id == destination_id:
                bot.sendMessage(destination_id, "Sorry to see you go... Type /start to start \
                    receiving updates again.")
                destination_id = -1

                try:
                    with open("destination_id.txt", "w") as file:
                        file.write(str(destination_id))
                except PermissionError:
                    print("Cannot erase current destination id, use will have to send the \
                        /stop command again!")


bot = telepot.Bot(os.getenv("BOT_TOKEN"))
MessageLoop(bot, handle_bot_message).run_as_thread()

old_data = get_data()  # get first round of data
schedule.every().minute.at(":00").do(send_prices)

print("Bot started!")

while True:
    schedule.run_pending()
    time.sleep(1)
