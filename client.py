
import aiohttp
import asyncio

import time
import json

async def run(loop):
    session = aiohttp.ClientSession()
    async with session.ws_connect('ws://localhost:8080/ws') as ws:
        await ws.send_str('request')
        count = 0
        start = time.time()
        async for msg in ws:
            if not count % 100 and time.time() - start > 10:
                break
            if msg.type == aiohttp.WSMsgType.TEXT:
                data = json.loads(msg.data)
                assert isinstance(data, list)
                count += 1
                await ws.send_str('request')
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break
        end = time.time()
        thruput = count / (end - start)
        print('thruput = ', thruput)
    

loop = asyncio.get_event_loop()
loop.run_until_complete(run(loop))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass