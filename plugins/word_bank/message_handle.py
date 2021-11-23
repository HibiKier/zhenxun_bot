from utils.utils import get_message_text
from utils.message_builder import image, at
from .rule import check
from .model import WordBank
from configs.path_config import DATA_PATH
from pathlib import Path
from nonebot.adapters.cqhttp import (
    Bot,
    GroupMessageEvent,
)
from nonebot.typing import T_State
from nonebot import on_message


__zx_plugin_name__ = "词库问答回复操作 [Hidden]"


data_dir = Path(DATA_PATH) / "word_bank"
data_dir.mkdir(parents=True, exist_ok=True)


message_handle = on_message(priority=7, block=True, rule=check)


@message_handle.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    path = data_dir / f"{event.group_id}"
    q = await WordBank.check(event.group_id, get_message_text(event.json()))
    placeholder_list = [
        (x.split("<_s>")[0], x.split("<_s>")[1])
        for x in q.format.split("<format>")[:-1]
    ] if q.format else []
    answer = ""
    _a = q.answer
    if not placeholder_list:
        answer = _a
    else:
        for idx, placeholder in placeholder_list:
            if placeholder.endswith("jpg"):
                answer += _a[:_a.find(f"[__placeholder_{idx}]")] + image(path / placeholder)
            else:
                answer += _a[:_a.find(f"[__placeholder_{idx}]")] + at(placeholder)
            _a = _a[_a.find(f"[__placeholder_{idx}]") + len(f"[__placeholder_{idx}]"):]
    await message_handle.send(answer)
