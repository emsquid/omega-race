import asyncio


class Thread:
    """
    The Thread represents a structure of control to run code in parallel

    :param target: Callable[[Any, Any], Awaitable[Any]], The coroutine to run
    :param args: Arguments for the target
    """

    def __init__(self, target, args=()):
        self.target = target
        self.args = args

    def start(self):
        """
        Create a task for the Thread to run
        """
        if asyncio.get_event_loop().is_running():
            asyncio.create_task(self.target(*self.args))


class Timer:
    """
    The Timer represents a structure of control to run code after an interval

    :param interval: float, The time to wait
    :param target: Callable[[Any, Any], Awaitable[Any]], The coroutine to run
    :param args: Arguments for the target
    """

    def __init__(self, interval: float, target, args=()):
        self.interval = interval
        self.target = target
        self.args = args

    async def _inner(self):
        await asyncio.sleep(self.interval)
        self.target(*self.args)

    def start(self):
        """
        Create a Thread for the Timer to run
        """
        Thread(self._inner).start()
