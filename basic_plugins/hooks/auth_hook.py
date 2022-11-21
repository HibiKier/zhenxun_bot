from typing import Optional

from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    Event,
)
from nonebot.matcher import Matcher
from nonebot.message import run_preprocessor, run_postprocessor
from nonebot.typing import T_State

from ._utils import (
    set_block_limit_false,
    AuthChecker,
)


# # 权限检测
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: Event):
    await AuthChecker().auth(matcher, bot, event)


# 解除命令block阻塞
@run_postprocessor
async def _(
        matcher: Matcher,
        exception: Optional[Exception],
        bot: Bot,
        event: Event,
        state: T_State,
):
    if not isinstance(event, MessageEvent) and matcher.plugin_name != "poke":
        return
    module = matcher.plugin_name
    set_block_limit_false(event, module)
