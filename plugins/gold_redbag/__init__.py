import random
import re
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from apscheduler.jobstores.base import JobLookupError
from nonebot import on_command, on_notice
from nonebot.adapters.onebot.v11 import (
    ActionFailed,
    Bot,
    GroupMessageEvent,
    Message,
    PokeNotifyEvent,
)
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.matcher import Matcher
from nonebot.message import IgnoredException, run_preprocessor
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me

from configs.config import NICKNAME
from configs.path_config import IMAGE_PATH
from services.log import logger
from utils.depends import AtList, GetConfig
from utils.message_builder import at, image
from utils.utils import is_number, scheduler

from .config import FESTIVE_KEY, GroupRedBag, RedBag
from .data_source import (
    build_open_result_image,
    check_gold,
    end_festive_red_bag,
    random_red_bag_background,
)

__zx_plugin_name__ = "金币红包"
__plugin_usage__ = """
usage：
    在群内发送指定金额的红包，拼手气项目
    指令：
        塞红包 [金币数] ?[红包数=5] ?[at指定人]: 塞入红包
        开/抢/*戳一戳*: 打开红包
        退回: 退回未开完的红包，必须在一分钟后使用
        示例：塞红包 1000
        示例：塞红包 1000 10
""".strip()
__plugin_superuser_usage__ = """
usage：
    节日全群红包指令
    指令：
        节日红包 [金额] [数量] ?[祝福语] ?[指定群]
""".strip()
__plugin_des__ = "运气项目又来了"
__plugin_cmd__ = [
    "塞红包 [金币数] ?[红包数=5] ?[at指定人]",
    "开/抢",
    "退回",
    "节日红包 [金额] [数量] ?[祝福语] ?[指定群] [_superuser]",
]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["金币红包", "塞红包"],
}
__plugin_cd_limit__ = {"rst": "急什么急什么，待会再发！"}
__plugin_configs__ = {
    "DEFAULT_TIMEOUT": {
        "value": 600,
        "help": "普通红包默认超时时间",
        "default_value": 600,
        "type": int,
    },
    "DEFAULT_INTERVAL": {
        "value": 60,
        "help": "用户发送普通红包最小间隔时间",
        "default_value": 60,
        "type": int,
    },
    "RANK_NUM": {
        "value": 10,
        "help": "结算排行显示前N位",
        "default_value": 10,
        "type": int,
    },
}
# __plugin_resources__ = {"prts": IMAGE_PATH}


async def rule(event: GroupMessageEvent) -> bool:
    return check_on_gold_red(event)


gold_red_bag = on_command(
    "塞红包", aliases={"金币红包"}, priority=5, block=True, permission=GROUP
)

open_ = on_command(
    "开", aliases={"抢"}, priority=5, block=True, permission=GROUP, rule=rule
)

poke_ = on_notice(priority=6, block=False)

return_ = on_command("退回", aliases={"退还"}, priority=5, block=True, permission=GROUP)

festive_redbag = on_command(
    "节日红包", priority=5, block=True, permission=SUPERUSER, rule=to_me()
)

GROUP_DATA: Dict[int, GroupRedBag] = {}

PATTERN = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~，。；‘、"""


# 阻断其他poke
# @run_preprocessor
# async def _(
#     matcher: Matcher,
#     event: PokeNotifyEvent,
# ):
#     try:
#         if matcher.type == "notice" and event.self_id == event.target_id:
#             flag = check_on_gold_red(event)
#             if flag:
#                 if matcher.plugin_name == "poke":
#                     raise IgnoredException("目前正在抢红包...")
#             else:
#                 if matcher.plugin_name == "gold_red_bag":
#                     raise IgnoredException("目前没有红包...")
#     except AttributeError:
#         pass


@gold_red_bag.handle()
async def _(
    bot: Bot,
    event: GroupMessageEvent,
    arg: Message = CommandArg(),
    at_list: List[int] = AtList(),
    default_interval: int = GetConfig(config="DEFAULT_INTERVAL"),
):
    group_red_bag: Optional[GroupRedBag] = GROUP_DATA.get(event.group_id)
    if not group_red_bag:
        group_red_bag = GroupRedBag(event.group_id)
        GROUP_DATA[event.group_id] = group_red_bag
    # 剩余过期时间
    time_remaining = group_red_bag.check_timeout(event.user_id)
    if time_remaining != -1:
        # 判断用户红包是否存在且是否过时覆盖
        if user_red_bag := group_red_bag.get_user_red_bag(event.user_id):
            now = time.time()
            if now < user_red_bag.start_time + default_interval:
                await gold_red_bag.finish(
                    f"你的红包还没消化完捏...还剩下 {user_red_bag.num - len(user_red_bag.open_user)} 个! 请等待红包领取完毕..."
                    f"(或等待{time_remaining}秒红包cd)"
                )
    msg = arg.extract_plain_text().strip().split()
    if not msg:
        await gold_red_bag.finish("不塞钱发什么红包！")
    amount = msg[0]
    if len(msg) == 1:
        flag, tip = await check_gold(str(event.user_id), str(event.group_id), amount)
        if not flag:
            await gold_red_bag.finish(tip, at_sender=True)
        num = 5
    else:
        num = msg[1]
        if not is_number(num) or int(num) < 1:
            await gold_red_bag.finish("红包个数给我输正确啊！", at_sender=True)
        flag, tip = await check_gold(str(event.user_id), str(event.group_id), amount)
        if not flag:
            await gold_red_bag.finish(tip, at_sender=True)
        group_member_num = (await bot.get_group_info(group_id=event.group_id))[
            "member_count"
        ]
        num = int(num)
        if num > group_member_num:
            await gold_red_bag.send("你发的红包数量也太多了，已经为你修改成与本群人数相同的红包数量...")
            num = group_member_num
    nickname = event.sender.card or event.sender.nickname
    await group_red_bag.add_red_bag(
        f"{nickname}的红包",
        int(amount),
        1 if at_list else num,
        nickname or "",
        str(event.user_id),
        assigner=str(at_list[0]) if at_list else None,
    )
    await gold_red_bag.send(
        f"{nickname}发起了金币红包\n金额: {amount}\n数量: {num}\n"
        + image(await random_red_bag_background(event.user_id))
    )
    logger.info(f"塞入 {num} 个红包，共 {amount} 金币", "金币红包", event.user_id, event.group_id)


@open_.handle()
async def _(
    event: GroupMessageEvent,
    arg: Message = CommandArg(),
    rank_num: int = GetConfig(config="RANK_NUM"),
):
    if msg := arg.extract_plain_text().strip():
        msg = re.sub(PATTERN, "", msg)
        if "红包" not in msg:
            return
    group_red_bag: Optional[GroupRedBag] = GROUP_DATA.get(event.group_id)
    if group_red_bag:
        open_data, settlement_list = await group_red_bag.open(event.user_id)
        send_msg = ""
        for _, item in open_data.items():
            amount, red_bag = item
            result_image = await build_open_result_image(red_bag, event.user_id, amount)
            send_msg += (
                f"开启了 {red_bag.promoter} 的红包, 获取 {amount} 个金币\n"
                + image(result_image)
                + "\n"
            )
            logger.info(
                f"抢到了 {red_bag.promoter}({red_bag.promoter_id}) 的红包，获取了{amount}个金币",
                "开红包",
                event.user_id,
                event.group_id,
            )
        send_msg = send_msg[:-1] if send_msg else "没有红包给你开！"
        await open_.send(send_msg, at_sender=True)
        if settlement_list:
            for red_bag in settlement_list:
                await open_.send(
                    f"{red_bag.name}已结算\n"
                    + image(await red_bag.build_amount_rank(rank_num))
                )


# @poke_.handle()
# async def _poke_(event: PokeNotifyEvent):
#     group_id = getattr(event, "group_id", None)
#     if event.self_id == event.target_id and group_id:
#         is_open = check_on_gold_red(event)
#         if not is_open:
#             return
#         group_red_bag: Optional[GroupRedBag] = GROUP_DATA.get(group_id)
#         if group_red_bag:
#             open_data, settlement_list = await group_red_bag.open(event.user_id)
#             send_msg = ""
#             for _, item in open_data.items():
#                 amount, red_bag = item
#                 result_image = await build_open_result_image(
#                     red_bag, event.user_id, amount
#                 )
#                 send_msg += (
#                     f"开启了 {red_bag.promoter} 的红包, 获取 {amount} 个金币\n"
#                     + image(result_image)
#                     + "\n"
#                 )
#                 logger.info(
#                     f"抢到了 {red_bag.promoter}({red_bag.promoter_id}) 的红包，获取了{amount}个金币",
#                     "开红包",
#                     event.user_id,
#                     event.group_id,
#                 )
#             if send_msg:
#                 await open_.send(send_msg, at_sender=True)
#                 if settlement_list:
#                     for red_bag in settlement_list:
#                         await open_.send(
#                             f"{red_bag.name}已结算\n"
#                             + image(await red_bag.build_amount_rank())
#                         )


@return_.handle()
async def _(
    event: GroupMessageEvent,
    default_interval: int = GetConfig(config="DEFAULT_INTERVAL"),
    rank_num: int = GetConfig(config="RANK_NUM"),
):
    group_red_bag: GroupRedBag = GROUP_DATA[event.group_id]
    if group_red_bag:
        if user_red_bag := group_red_bag.get_user_red_bag(event.user_id):
            now = time.time()
            if now - user_red_bag.start_time < default_interval:
                await return_.finish(
                    f"你的红包还没有过时, 在 {int(default_interval - now + user_red_bag.start_time)} "
                    f"秒后可以退回...",
                    at_sender=True,
                )
            user_red_bag = group_red_bag.get_user_red_bag(event.user_id)
            if user_red_bag and (
                return_amount := await group_red_bag.settlement(event.user_id)
            ):
                logger.info(
                    f"退回了红包 {return_amount} 金币", "红包退回", event.user_id, event.group_id
                )
                await return_.send(
                    f"已成功退还了 "
                    f"{return_amount} 金币\n"
                    + image(await user_red_bag.build_amount_rank(rank_num)),
                    at_sender=True,
                )
    await return_.send("目前没有红包可以退回...", at_sender=True)


@festive_redbag.handle()
async def _(bot: Bot, arg: Message = CommandArg()):
    global redbag_data
    msg = arg.extract_plain_text().strip()
    if msg:
        msg = msg.split()
        amount = 0
        num = 0
        greetings = "恭喜发财 大吉大利"
        gl = []
        if (lens := len(msg)) < 2:
            await festive_redbag.finish("参数不足，格式：节日红包 [金额] [数量] [祝福语](可省) [指定群](可省)")
        if lens > 1:
            if not is_number(msg[0]):
                await festive_redbag.finish("金额必须要是数字！", at_sender=True)
            amount = int(msg[0])
            if not is_number(msg[1]):
                await festive_redbag.finish("数量必须要是数字！", at_sender=True)
            num = int(msg[1])
            if lens > 2:
                greetings = msg[2]
            if lens > 3:
                for i in range(3, lens):
                    if not is_number(msg[i]):
                        await festive_redbag.finish("指定的群号必须要是数字啊！", at_sender=True)
                    gl.append(int(msg[i]))
        if not gl:
            gl = await bot.get_group_list()
            gl = [g["group_id"] for g in gl]
        for g in gl:
            group_red_bag: Optional[GroupRedBag] = GROUP_DATA.get(g)
            if not group_red_bag:
                group_red_bag = GroupRedBag(g)
                GROUP_DATA[g] = group_red_bag
            try:
                scheduler.remove_job(f"{FESTIVE_KEY}_{g}")
                await end_festive_red_bag(bot, group_red_bag)
            except JobLookupError:
                pass
            await group_red_bag.add_red_bag(
                f"{NICKNAME}的红包", int(amount), num, NICKNAME, FESTIVE_KEY, True
            )
            scheduler.add_job(
                end_festive_red_bag,
                "date",
                # run_date=(datetime.now() + timedelta(hours=24)).replace(microsecond=0),
                run_date=(datetime.now() + timedelta(seconds=30)).replace(
                    microsecond=0
                ),
                id=f"{FESTIVE_KEY}_{g}",
                args=[bot, group_red_bag],
            )
            try:
                await bot.send_group_msg(
                    group_id=g,
                    message=f"{NICKNAME}发起了金币红包\n金额：{amount}\n数量：{num}\n"
                    + image(await random_red_bag_background(bot.self_id, greetings)),
                )
                logger.debug("节日红包图片信息发送成功...", "节日红包", group_id=g)
            except ActionFailed:
                logger.warning(f"节日红包图片信息发送失败...", "节日红包", group_id=g)


def check_on_gold_red(event) -> bool:
    if group_red_bag := GROUP_DATA.get(event.group_id):
        return group_red_bag.check_open(event.user_id)
    return False
