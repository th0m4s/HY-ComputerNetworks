# step_c.py
# ENE0419 - Computer Networks - Assignment 3
# Thomas LEDOS (9201320221) - https://github.com/th0m4s/HY-ComputerNetworks

import asyncio
import websockets
import json


async def handle_upbit(file):
    async with websockets.connect("wss://api.upbit.com/websocket/v1") as ws:
        print("Connected to Upbit!")
        await ws.send(json.dumps([{"ticket": "UNIQUE_TICKET"}, {"type": "orderbook", "codes": ["KRW-BTC"]}]))
        print("Subscribed to Upbit stream!")
        async for message in ws:
            data = json.loads(message)
            file.write("btckrw@orderbook," + json.dumps(data["orderbook_units"]) + "\n")
            file.flush()


async def handle_binance(file):
    async with websockets.connect("wss://stream.binance.com/ws/v1") as ws:
        print("Connected to Binance!")
        await ws.send(json.dumps({"method": "SUBSCRIBE", "params": ["btcusdt@depth5", "btcusdt@trade"], "id": 1}))
        await ws.recv()
        print("Subscribed to Binance streams!")
        async for message in ws:
            data = json.loads(message)
            if "bids" in data:
                file.write("btcusdt@orderbook,bids:" + json.dumps(data["bids"]) + ",asks:" + json.dumps(data["asks"]) + "\n")
            else:
                file.write("btcusdt@trade," + json.dumps({"p": data["p"], "q": data["q"]}) + "\n")
            file.flush()


async def connect():
    file = open("stream-data-multi.txt", "w")
    await asyncio.wait([
        handle_upbit(file),
        handle_binance(file),
    ])


asyncio.get_event_loop().run_until_complete(connect())
