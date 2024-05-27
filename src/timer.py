import asyncio
from threading import Thread


def timer(interval: float, function, args=()):
    async def inner():
        await asyncio.sleep(interval)
        function(*args)

    Thread(target=inner).start()
