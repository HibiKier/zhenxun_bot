from typing import Union

from nonebot.adapters.onebot.v11 import Bot as V11Bot
from nonebot.adapters.onebot.v12 import Bot as V12Bot


def check_user_id(bot: Union[V11Bot, V12Bot], user_id: str) -> bool:
    platform = "qq" if isinstance(bot, V11Bot) else bot.platform

    if platform == "qq":
        return user_id.isdigit() and 11 >= len(user_id) >= 5

    return False
