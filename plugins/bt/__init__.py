from nonebot import on_command
from .data_source import get_bt_info
from services.log import logger
from nonebot.typing import T_State
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import PrivateMessageEvent
from utils.utils import get_message_text
from nonebot.adapters.cqhttp.permission import PRIVATE
from utils.utils import UserExistLimiter
from asyncio.exceptions import TimeoutError
from aiohttp.client_exceptions import ServerDisconnectedError

__plugin_name__ = "磁力搜索"
__plugin_usage__ = r"""
* 请各位使用后不要转发 *
* 拒绝反冲斗士！ *
bt [关键词] [页数](默认为1)
示例：
bt 钢铁侠
bt 钢铁侠 3
""".strip()

_ulmt = UserExistLimiter()

bt = on_command("bt", permission=PRIVATE, priority=5, block=True)


@bt.args_parser
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    if str(event.get_message()) in ["取消", "算了"]:
        await bt.finish("已取消操作..", at_sender=True)
    msg = get_message_text(event.json())
    if not msg:
        await bt.reject("你想搜索什么呢？", at_sender=True)
    state["keyword"] = msg
    state["page"] = "1"


@bt.handle()
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    if _ulmt.check(event.user_id):
        await bt.finish("您有bt任务正在进行，请等待结束.", at_sender=True)
    mp = get_message_text(event.json())
    if not mp:
        return
    mp = mp.split()
    if len(mp) == 2:
        state["keyword"] = mp[0]
        state["page"] = mp[1]
    else:
        state["keyword"] = mp[0]
        state["page"] = "1"


@bt.got("keyword", prompt="虚空磁力？查什么GKD")
async def _(bot: Bot, event: PrivateMessageEvent, state: T_State):
    _ulmt.set_True(event.user_id)
    keyword = state["keyword"]
    page = state["page"]
    await bt.send("开始搜索....", at_sender=True)
    send_flag = False
    try:
        async for title, itype, create_time, file_size, link in get_bt_info(
            keyword, page
        ):
            await bt.send(
                f"标题：{title}\n"
                f"类型：{itype}\n"
                f"创建时间：{create_time}\n"
                f"文件大小：{file_size}\n"
                f"种子：{link}"
            )
            send_flag = True
    except TimeoutError:
        _ulmt.set_False(event.user_id)
        await bt.finish(f"搜索 {keyword} 超时...")
    except ServerDisconnectedError:
        _ulmt.set_False(event.user_id)
        await bt.finish(f"搜索 {keyword} 连接失败")
    except Exception as e:
        _ulmt.set_False(event.user_id)
        await bt.finish(f"bt 其他未知错误..")
        logger.error(f"bt 错误 e：{e}")
    if not send_flag:
        await bt.send(f"{keyword} 未搜索到...")
    logger.info(f"USER {event.user_id} BT搜索 {keyword} 第 {page} 页")
    _ulmt.set_False(event.user_id)
