import asyncio
import threading

class AsyncLoop:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        t = threading.Thread(target=self.loop.run_forever, daemon=True)
        t.start()

    def run(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self.loop)

async_loop = AsyncLoop()