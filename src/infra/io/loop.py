import asyncio
from asyncio.events import AbstractEventLoop

import aiotask_context as context


class MainIOLoop():
    @staticmethod
    def setup() -> AbstractEventLoop:
        _loop = asyncio.get_event_loop()
        _loop.set_task_factory(factory=context.task_factory)
        return _loop