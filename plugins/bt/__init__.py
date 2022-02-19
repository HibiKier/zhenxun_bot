from nonebot import on_command
from .data_source import get_bt_info
from services.log import logger
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, Message
from nonebot.adapters.onebot.v11.permission import PRIVATE
from asyncio.exceptions import TimeoutError
from utils.utils import is_number
from nonebot.params import CommandArg, ArgStr
from nonebot.typing import T_State

__zx_plugin_name__ = "磁力搜索"
__plugin_usage__ = """
usage：
    * 请各位使用后不要转发 *
    * 拒绝反冲斗士！ *
    指令：
        bt [关键词] ?[页数]
        示例：bt 钢铁侠
        示例：bt 钢铁侠 3
""".strip()
__plugin_des__ = "bt(磁力搜索)[仅支持私聊，懂的都懂]"
__plugin_cmd__ = ["bt [关键词] ?[页数]"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["bt", "磁力搜索", "Bt", "BT"],
}
__plugin_block_limit__ = {"rst": "您有bt任务正在进行，请等待结束."}
__plugin_configs__ = {
    "BT_MAX_NUM": {
        "value": 10,
        "help": "单次BT搜索返回最大消息数量",
        "default_value": 10,
    }
}


bt = on_command("bt", permission=PRIVATE, priority=5, block=True)


@bt.handle()
async def _(state: T_State, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip().split()
    if msg:
        keyword = None
        page = 1
        if n := len(msg):
            keyword = msg[0]
        if n > 1 and is_number(msg[1]) and int(msg[1]) > 0:
            page = int(msg[1])
        state["keyword"] = keyword
        state["page"] = page
    else:
        state["page"] = 1


@bt.got("keyword", prompt="请输入要查询的内容！")
async def _(
    event: PrivateMessageEvent,
    state: T_State,
    keyword: str = ArgStr("keyword"),
    page: str = ArgStr("page"),
):
    send_flag = False
    try:
        async for title, type_, create_time, file_size, link in get_bt_info(
            keyword, page
        ):
            await bt.send(
                f"标题：{title}\n"
                f"类型：{type_}\n"
                f"创建时间：{create_time}\n"
                f"文件大小：{file_size}\n"
                f"种子：{link}"
            )
            send_flag = True
    except TimeoutError:
        await bt.finish(f"搜索 {keyword} 超时...")
    except Exception as e:
        await bt.finish(f"bt 其他未知错误..")
        logger.error(f"bt 错误 {type(e)}：{e}")
    if not send_flag:
        await bt.send(f"{keyword} 未搜索到...")
    logger.info(f"USER {event.user_id} BT搜索 {keyword} 第 {page} 页")
