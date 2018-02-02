
import aiohttp
import asyncio

import time
import json

async def run(loop):
    session = aiohttp.ClientSession()
    async with session.ws_connect('ws://localhost:8080/ws') as ws:
        
        count = 0
        start = time.time()
        await ws.send_str('stats')
        start_d = await ws.receive()
        start_d = json.loads(start_d.data)
        await ws.send_str('request')
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
        await ws.send_str('stats')
        end_d = await ws.receive()
        end_d = json.loads(end_d.data)
        end = time.time()
        thruput = count / (end - start)
        print('thruput = ', int(thruput))
        print('light = ', end_d['light'] - start_d['light'])
        print('heavy = ', end_d['heavy'] - start_d['heavy'])
    

loop = asyncio.get_event_loop()
loop.run_until_complete(run(loop))
