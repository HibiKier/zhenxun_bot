import asyncio
from collections.abc import Awaitable, Callable
from typing import Generic, TypeVar

_T = TypeVar("_T")
LogListener = Callable[[_T], Awaitable[None]]


class LogStorage(Generic[_T]):
    """
    日志存储
    """

    def __init__(self, rotation: float = 5 * 60):
        self.count, self.rotation = 0, rotation
        self.logs: dict[int, str] = {}
        self.listeners: set[LogListener[str]] = set()

    async def add(self, log: str):
        seq = self.count = self.count + 1
        self.logs[seq] = log
        asyncio.get_running_loop().call_later(self.rotation, self.remove, seq)
        await asyncio.gather(
            *(listener(log) for listener in self.listeners),
            return_exceptions=True,
        )
        return seq

    def remove(self, seq: int):
        del self.logs[seq]


LOG_STORAGE: LogStorage[str] = LogStorage[str]()
