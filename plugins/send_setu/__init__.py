import random
from nonebot import on_command, on_regex
from services.log import logger
from models.sigin_group_user import SignGroupUser
from nonebot.exception import IgnoredException
from nonebot.message import run_preprocessor, run_postprocessor
from nonebot.matcher import Matcher
from typing import Optional, Type
from gino.exceptions import UninitializedError
from utils.utils import (
    FreqLimiter,
    UserExistLimiter,
    is_number,
    get_message_text,
    get_message_imgs,
)
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import (
    Bot,
    MessageEvent,
    GroupMessageEvent,
    PrivateMessageEvent,
    Message,
    Event,
)
from .data_source import (
    get_setu_list,
    get_luoxiang,
    search_online_setu,
    get_setu_urls,
    find_img_index,
    gen_message,
    check_local_exists_or_download,
    add_data_to_database,
)
from nonebot.adapters.cqhttp.exception import ActionFailed
from configs.config import ONLY_USE_LOCAL_SETU, WITHDRAW_SETU_TIME
from utils.message_builder import at
import re
import asyncio

try:
    import ujson as json
except ModuleNotFoundError:
    import json

__plugin_name__ = "色图"
__plugin_usage__ = f"""示例：
    1. 色图   （随机本地色图）
    2. 色图r   （随机在线十张r18涩图）
    3. 色图 666 （本地色图id）
    4. 色图 xx xx （在线搜索xx xx色图）
    5. 色图r xx   （搜索十张xx的r18涩图，注意空格）（仅私聊，每日限制5次）
    6. 来n张涩图  （本地涩图连发）（1<=n<=9）
    7. 来n张xx的涩图   （在线搜索xx涩图）（较慢，看网速）
注：
    xx 为 tag，多余20取前20 示例：原神 黑丝
    本地涩图没有r18！
    联网搜索会较慢！
    如果图片数量与数字不符，
    原因1：网络不好，网线被拔QAQ
    原因2：搜索到的总数小于数字
    原因3：图太色或者小错误了】"""

_flmt = FreqLimiter(5)
_ulmt = UserExistLimiter()
setu_data_list = []
withdraw_message_id = []


@run_preprocessor
async def _(matcher: Matcher, bot: Bot, event: MessageEvent, state: T_State):
    if isinstance(event, MessageEvent):
        if matcher.module == "send_setu":
            if _ulmt.check(event.user_id):
                if isinstance(event, GroupMessageEvent):
                    await bot.send_group_msg(
                        group_id=event.group_id,
                        message=Message(f"{at(event.user_id)}您有色图正在处理，请稍等....."),
                    )
                else:
                    await bot.send_private_msg(
                        user_id=event.user_id, message=f"您有色图正在处理，请稍等....."
                    )
                raise IgnoredException("色图正在处理！")
            _ulmt.set_True(event.user_id)


@run_postprocessor
async def do_something(
    matcher: Matcher,
    exception: Optional[Exception],
    bot: Bot,
    event: Event,
    state: T_State,
):
    global setu_data_list, withdraw_message_id
    if isinstance(event, MessageEvent):
        if matcher.module == "send_setu":
            # 解除占用
            _ulmt.set_False(event.user_id)
            tasks = []
            # 撤回色图
            for id_ in withdraw_message_id[:]:
                tasks.append(asyncio.ensure_future(withdraw_message(bot, event, id_)))
                withdraw_message_id.remove(id_)
            await asyncio.gather(*tasks)
            # 添加数据至数据库
            try:
                await add_data_to_database(setu_data_list)
                logger.info("色图数据自动存储数据库成功...")
                setu_data_list = []
            except UninitializedError:
                pass


setu = on_command(
    "色图", aliases={"涩图", "不够色", "来一发", "再来点", "色图r"}, priority=5, block=True
)

setu_reg = on_regex("(.*)[份|发|张|个|次|点](.*)[瑟|色|涩]图", priority=5, block=True)

find_setu = on_command("查色图", priority=5, block=True)


@setu.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    global withdraw_message_id
    msg = get_message_text(event.json())
    if isinstance(event, GroupMessageEvent):
        impression = (
            await SignGroupUser.ensure(event.user_id, event.group_id)
        ).impression
        luox = get_luoxiang(impression)
        if luox:
            await setu.finish(luox)
    if not _flmt.check(event.user_id):
        await setu.finish("您冲得太快了，请稍候再冲", at_sender=True)
    _flmt.start_cd(event.user_id)
    r18 = 0
    num = 1
    # 是否看r18
    if state["_prefix"]["raw_command"] == "色图r" and isinstance(
        event, PrivateMessageEvent
    ):
        r18 = 1
        num = 10
    elif state["_prefix"]["raw_command"] == "色图r" and isinstance(
        event, GroupMessageEvent
    ):
        await setu.finish(
            random.choice(["这种不好意思的东西怎么可能给这么多人看啦", "羞羞脸！给我滚出克私聊！", "变态变态变态变态大变态！"])
        )
    # 有 数字 的话先尝试本地色图id
    if msg and is_number(msg):
        setu_list, code = await get_setu_list(int(msg), r18=r18)
        if code != 200:
            await setu.finish(setu_list[0], at_sender=True)
        setu_img, code = await check_local_exists_or_download(setu_list[0])
        msg_id = await setu.send(gen_message(setu_list[0]) + setu_img, at_sender=True)
        logger.info(
            f"(USER {event.user_id}, GROUP "
            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
            f" 发送色图 {setu_list[0].local_id}.png"
        )
        withdraw_message_id.append(msg_id["message_id"])
        return
    await send_setu_handle(setu, event, state["_prefix"]["raw_command"], msg, num, r18)


num_key = {
    "一": 1,
    "二": 2,
    "两": 2,
    "双": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
}


@setu_reg.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if isinstance(event, GroupMessageEvent):
        impression = (
            await SignGroupUser.ensure(event.user_id, event.group_id)
        ).impression
        luox = get_luoxiang(impression)
        if luox:
            await setu.finish(luox, at_sender=True)
    if not _flmt.check(event.user_id):
        await setu.finish("您冲得太快了，请稍候再冲", at_sender=True)
    _flmt.start_cd(event.user_id)
    msg = get_message_text(event.json())
    num = 1
    msg = re.search(r"(.*)[份发张个次点](.*)[瑟涩色]图", msg)
    # 解析 tags 以及 num
    if msg:
        num = msg.group(1)
        tags = msg.group(2)
        if tags:
            tags = tags[:-1] if tags[-1] == "的" else tags
        if num:
            num = num[-1]
            if num_key.get(num):
                num = num_key[num]
            elif is_number(num):
                try:
                    num = int(num)
                except ValueError:
                    num = 1
            else:
                num = 1
    else:
        return
    await send_setu_handle(setu_reg, event, '色图', tags, num, 0)


@find_setu.args_parser
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if str(event.message) == "取消":
        await find_setu.finish("取消了操作", at_sender=True)
    imgs = get_message_imgs(event.json())
    if not imgs:
        await find_setu.reject("不搞错了，俺要图！")
    state["img"] = imgs[0]


@find_setu.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if get_message_text(event.json()) in ["帮助"]:
        await find_setu.finish("通过图片获取本地色图id\n\t示例：查色图(图片)")
    imgs = get_message_imgs(event.json())
    if imgs:
        state["img"] = imgs[0]


@find_setu.got("img", prompt="速速来图！")
async def _(bot: Bot, event: MessageEvent, state: T_State):
    img = state["img"]
    await find_setu.send(await find_img_index(img, event.user_id), at_sender=True)


async def send_setu_handle(
    matcher: Type[Matcher], event: MessageEvent, command: str, msg: str, num: int, r18: int
):
    global setu_data_list, withdraw_message_id
    error_info = ""
    # 非 id，在线搜索
    tags = msg.split()
    # 真寻的色图？怎么可能
    if "真寻" in tags:
        await matcher.finish("咳咳咳，虽然我很可爱，但是我木有自己的色图~~~有的话记得发我一份呀")
    # 本地先拿图，下载失败补上去
    setu_list, code = await get_setu_list(tags=msg.split(), r18=r18)
    if not ONLY_USE_LOCAL_SETU and (tags or not setu_list or num > len(setu_list)):
        # 先尝试获取在线图片
        urls, text_list, add_databases_list, code = await get_setu_urls(tags, num, r18, command)
        for x in add_databases_list:
            setu_data_list.append(x)
        # 未找到符合的色图，想来本地应该也没有
        if code == 401:
            await setu.finish(urls[0], at_sender=True)
        if code == 200:
            for i in range(len(urls)):
                try:
                    setu_img, index = await search_online_setu(urls[i])
                    # 下载成功的话
                    if index != -1:
                        logger.info(
                            f"(USER {event.user_id}, GROUP "
                            f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
                            f" 发送色图 {index}.png"
                        )
                        msg_id = await matcher.send(Message(f"{text_list[i]}\n{setu_img}"))
                        withdraw_message_id.append(msg_id["message_id"])
                    else:
                        if setu_list:
                            setu_image = random.choice(setu_list)
                            setu_list.remove(setu_image)
                            msg_id = await matcher.send(
                                Message(
                                    gen_message(setu_image)
                                    + (await check_local_exists_or_download(setu_image))[0]
                                )
                            )
                            logger.info(
                                f"(USER {event.user_id}, GROUP "
                                f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
                                f" 发送本地色图 {setu_image.local_id}.png"
                            )
                        else:
                            msg_id = await matcher.send(text_list[i] + "\n" + setu_img)
                        withdraw_message_id.append(msg_id["message_id"])
                except ActionFailed:
                    await matcher.finish("坏了，这张图色过头了，我自己看看就行了！", at_sender=True)
            return
    # 本地无图 或 超过上下限
    if code != 200 or (not setu_list and ONLY_USE_LOCAL_SETU):
        await matcher.finish(setu_list[0], at_sender=True)
    elif not setu_list:
        await matcher.finish(error_info, at_sender=True)
    # 开始发图
    for _ in range(num):
        if not setu_list:
            await setu.finish("坏了，已经没图了，被榨干了！")
        setu_image = random.choice(setu_list)
        setu_list.remove(setu_image)
        try:
            msg_id = await matcher.send(
                Message(
                    gen_message(setu_image)
                    + (await check_local_exists_or_download(setu_image))[0]
                )
            )
            withdraw_message_id.append(msg_id["message_id"])
            logger.info(
                f"(USER {event.user_id}, GROUP "
                f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
                f" 发送本地色图 {setu_image.local_id}.png"
            )
        except ActionFailed:
            await matcher.finish("坏了，这张图色过头了，我自己看看就行了！", at_sender=True)


# 撤回图片
async def withdraw_message(bot: Bot, event: MessageEvent, id_: int):
    if WITHDRAW_SETU_TIME[0]:
        if (
            (WITHDRAW_SETU_TIME[1] == 0 and isinstance(event, PrivateMessageEvent))
            or (WITHDRAW_SETU_TIME[1] == 1 and isinstance(event, GroupMessageEvent))
            or WITHDRAW_SETU_TIME[1] == 2
        ):
            await asyncio.sleep(WITHDRAW_SETU_TIME[0])
            await bot.delete_msg(message_id=id_, self_id=int(bot.self_id))
            logger.info(f"自动撤回色图 消息id：{id_}")
