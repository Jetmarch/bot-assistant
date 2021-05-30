import asyncio
from application import Application


app = Application()
loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(app.launch_bot())
finally:
    loop.close()