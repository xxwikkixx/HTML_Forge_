import asyncio
import time

async def display_date(loop):
    print("process:", loop, "is started")
    time.sleep(3)
    print("process:", loop, "is done")


asyncio.get_event_loop().run_until_complete(display_date(1))
asyncio.get_event_loop().run_until_complete(display_date(2))
asyncio.get_event_loop().run_until_complete(display_date(3))
asyncio.get_event_loop().run_until_complete(display_date(4))
asyncio.get_event_loop().run_until_complete(display_date(5))
asyncio.get_event_loop().run_until_complete(display_date(6))
asyncio.get_event_loop().run_until_complete(display_date(7))

asyncio.get_event_loop().close()