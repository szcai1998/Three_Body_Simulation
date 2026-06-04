import asyncio
import websockets

async def test():
    try:
        async with websockets.connect("ws://localhost:8000/ws/simulation") as ws:
            print("Connected!")
            # wait for state
            res = await ws.recv()
            print("Received bytes:", len(res))
    except Exception as e:
        print("Error:", e)

asyncio.run(test())
