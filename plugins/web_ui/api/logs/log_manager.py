import asyncio
import re
from typing import Awaitable, Callable, ClassVar, Dict, Generic, List, Set, TypeVar
from urllib.parse import urlparse

PATTERN = r"\x1b(\[.*?[@-~]|\].*?(\x07|\x1b\\))"

_T = TypeVar("_T")
LogListener = Callable[[_T], Awaitable[None]]


class LogStorage(Generic[_T]):
    def __init__(self, rotation: float = 5 * 60):
        self.count, self.rotation = 0, rotation
        self.logs: Dict[int, str] = {}
        self.listeners: Set[LogListener[str]] = set()

    async def add(self, log: str):
        log = re.sub(PATTERN, "", log)
        log_split = log.split()
        time = log_split[0] + " " + log_split[1]
        level = log_split[2]
        main = log_split[3]
        type_ = None
        log_ = " ".join(log_split[3:])
        if "Calling API" in log_:
            sp = log_.split("|")
            type_ = sp[1]
            log_ = "|".join(log_[1:])
        data = {"time": time, "level": level, "main": main, "type": type_, "log": log_}
        seq = self.count = self.count + 1
        self.logs[seq] = log
        asyncio.get_running_loop().call_later(self.rotation, self.remove, seq)
        await asyncio.gather(
            *map(lambda listener: listener(log), self.listeners),
            return_exceptions=True,
        )
        return seq

    def remove(self, seq: int):
        del self.logs[seq]
        return


LOG_STORAGE = LogStorage[str]()
