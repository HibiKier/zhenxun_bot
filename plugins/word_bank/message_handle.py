from nonebot import on_message
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageEvent
from nonebot.typing import T_State

from configs.path_config import DATA_PATH
from services import logger

from ._model import WordBank
from ._rule import check

__zx_plugin_name__ = "词库问答回复操作 [Hidden]"

data_dir = DATA_PATH / "word_bank"
data_dir.mkdir(parents=True, exist_ok=True)

message_handle = on_message(priority=6, block=True, rule=check)


@message_handle.handle()
async def _(event: MessageEvent, state: T_State):
    if problem := state.get("problem"):
        if msg := await WordBank.get_answer(event, problem):
            await message_handle.send(msg)
            logger.info(
                f" 触发词条 {problem}",
                "词条检测",
                event.user_id,
                getattr(event, "group_id", None),
            )
