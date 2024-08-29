import time

import nonebot
from nonebot.adapters.onebot.v11 import Bot
from nonebot.drivers import Driver

driver: Driver = nonebot.get_driver()


class BotLive:
    def __init__(self):
        self._data = {}

    def add(self, bot_id: str):
        self._data[bot_id] = time.time()

    def get(self, bot_id: str) -> int | None:
        return self._data.get(bot_id)

    def remove(self, bot_id: str):
        if bot_id in self._data:
            del self._data[bot_id]


bot_live = BotLive()


@driver.on_bot_connect
async def _(bot: Bot):
    bot_live.add(bot.self_id)


@driver.on_bot_disconnect
async def _(bot: Bot):
    bot_live.remove(bot.self_id)
