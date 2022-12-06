# step_a.py
# ENE0419 - Computer Networks - Assignment 3
# Thomas LEDOS (9201320221) - https://github.com/th0m4s/HY-ComputerNetworks

import asyncio
import websockets
import json


async def handle_socket(host, file):
    async with websockets.connect(host) as ws:
        print("Connected!")
        await ws.send('{"method": "SUBSCRIBE", "params": ["btcusdt@depth5", "btcusdt@trade"], "id": 1}')
        print(await ws.recv())
        print("Subscribed!")

        async for message in ws:
            data = json.loads(message)

            if "bids" in data:
                file.write("btcusdt@orderbook,bids:" + json.dumps(data["bids"]) + ",asks:" + json.dumps(data["asks"]) + "\n")
            else:
                file.write("btcusdt@trade," + json.dumps({"p": data["p"], "q": data["q"]}) + "\n")
            file.flush()


async def connect():
    file = open("stream-data-single.txt", "w")
    await handle_socket("wss://stream.binance.com/ws/v1", file)


asyncio.get_event_loop().run_until_complete(connect())
