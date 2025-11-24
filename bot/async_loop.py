import asyncio
import threading
import atexit

class AsyncLoop:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def _run_loop(self):
        asyncio.set_event_loop(self.loop)
        try:
            self.loop.run_forever()
        finally:
            # Не закрываем цикл здесь, пусть работает до конца программы
            pass

    def run(self, coro):
        try:
            return asyncio.run_coroutine_threadsafe(coro, self.loop)
        except RuntimeError:
            # Если цикл закрыт, игнорируем ошибку
            return None

# Глобальный экземпляр
async_loop = AsyncLoop()

def cleanup():
    """Упрощенная очистка - не пытаемся выполнять асинхронные операции при выходе"""
    pass

atexit.register(cleanup)