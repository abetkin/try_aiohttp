
import random
import asyncio
import time
from aiohttp import web

import asyncio
import aiopg

dsn = 'dbname=mydb user=postgres password=postgres host=127.0.0.1'

import json


async def websocket_handler(request):
    ws = web.WebSocketResponse(autoclose=False)
    await ws.prepare(request)
    async for msg in ws:
        if msg.data != 'request':
            continue
        if random.randrange(5):
            await ws.send_str('[]')
            continue
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT value FROM app_int WHERE value > 333")
                ret = []
                async for row in cur:
                    ret.append(row[0])
                msg = json.dumps(ret)
                await ws.send_str(msg)

    return ws

async def init(loop):
    app = web.Application()
    app.router.add_route('GET', '/ws', websocket_handler)
    global pool
    pool = await aiopg.create_pool(dsn)
    srv = await loop.create_server(
        app.make_handler(), '0.0.0.0', 8080)
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# 350