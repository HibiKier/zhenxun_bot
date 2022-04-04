from utils.message_builder import image, at
from ._rule import check
from .model import WordBank
from configs.path_config import DATA_PATH
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from utils.utils import get_message_text
from nonebot import on_message
from models.group_member_info import GroupInfoUser

__zx_plugin_name__ = "词库问答回复操作 [Hidden]"

data_dir = DATA_PATH / "word_bank"
data_dir.mkdir(parents=True, exist_ok=True)

message_handle = on_message(priority=6, block=True, rule=check)


@message_handle.handle()
async def _(event: GroupMessageEvent):
    q = await WordBank.check(
        event.group_id, get_message_text(event.json()), event.is_tome()
    )
    await message_handle.send(await get_one_answer(event, q.format, q.answer))


# 处理单条回答
async def get_one_answer(event, format, _answer, all=1):
    path = data_dir / f"{event.group_id}"
    placeholder_list = (
        [
            (x.split("<_s>")[0], x.split("<_s>")[1])
            for x in format.split("<format>")[:-1]
        ]
        if format
        else []
    )
    answer = ""
    _a = _answer
    if not placeholder_list:
        answer = _a
        return answer
    else:
        for idx, placeholder in placeholder_list:
            if placeholder.endswith("jpg"):
                answer += _a[: _a.find(f"[__placeholder_{idx}]")] + image(
                    path / placeholder
                )
            else:
                if all == 1:
                    answer += _a[: _a.find(f"[__placeholder_{idx}]")] + at(placeholder)
                else:
                    q = await GroupInfoUser.get_member_info(
                        int(placeholder), event.group_id)
                    answer += _a[: _a.find(f"[__placeholder_{idx}]")] + "@" + q.user_name
            _a = _a[_a.find(f"[__placeholder_{idx}]") + len(f"[__placeholder_{idx}]"):]
    return answer + _a
