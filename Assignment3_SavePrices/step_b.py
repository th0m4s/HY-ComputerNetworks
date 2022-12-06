# step_b.py
# ENE0419 - Computer Networks - Assignment 3
# Thomas LEDOS (9201320221) - https://github.com/th0m4s/HY-ComputerNetworks

import asyncio
import websockets
import json


async def handle_socket(host, file):
    async with websockets.connect(host) as ws:
        print("Connected!")
        await ws.send(json.dumps([{"ticket": "UNIQUE_TICKET"}, {"type": "orderbook", "codes": ["KRW-BTC"]}]))
        print("Subscribed!")

        async for message in ws:
            data = json.loads(message)

            file.write("btckrw@orderbook," + json.dumps(data["orderbook_units"]) + "\n")
            file.flush()


async def connect():
    file = open("stream-data-upbit.txt", "w")
    await handle_socket("wss://api.upbit.com/websocket/v1", file)


asyncio.get_event_loop().run_until_complete(connect())
