from nonebot import on_command, on_notice
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    PokeNotifyEvent,
    Message
)
from .data_source import (
    check_gold,
    generate_send_redbag_pic,
    open_redbag,
    generate_open_redbag_pic,
    return_gold,
)
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.message import run_preprocessor, IgnoredException
from nonebot.matcher import Matcher
from utils.utils import is_number, scheduler
from utils.message_builder import image
from services.log import logger
from configs.path_config import IMAGE_PATH
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from datetime import datetime, timedelta
from configs.config import NICKNAME
from apscheduler.jobstores.base import JobLookupError
from nonebot.adapters.onebot.v11.exception import ActionFailed
from nonebot.params import CommandArg
import random
import time


__zx_plugin_name__ = "金币红包"
__plugin_usage__ = """
usage：
    在群内发送指定金额的红包，拼手气项目
    指令：
        塞红包 [金币数] ?[红包数=5]: 塞入红包
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
    "塞红包 [金币数] ?[红包数=5]",
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
__plugin_resources__ = {"prts": IMAGE_PATH}

gold_redbag = on_command(
    "塞红包", aliases={"金币红包"}, priority=5, block=True, permission=GROUP
)

open_ = on_command("开", aliases={"抢"}, priority=5, block=True, permission=GROUP)

poke_ = on_notice(priority=6, block=False)

return_ = on_command("退回", aliases={"退还"}, priority=5, block=True, permission=GROUP)

festive_redbag = on_command(
    "节日红包", priority=5, block=True, permission=SUPERUSER, rule=to_me()
)

redbag_data = {}

festive_redbag_data = {}


# 阻断其他poke
@run_preprocessor
async def _(matcher: Matcher, event: PokeNotifyEvent):
    try:
        if matcher.type == "notice" and event.self_id == event.target_id:
            flag1 = True
            flag2 = True
            try:
                if festive_redbag_data[event.group_id]["user_id"]:
                    if (
                        event.user_id
                        in festive_redbag_data[event.group_id]["open_user"]
                    ):
                        flag1 = False
            except KeyError:
                flag1 = False
            try:
                if redbag_data[event.group_id]["user_id"]:
                    if event.user_id in redbag_data[event.group_id]["open_user"]:
                        flag2 = False
            except KeyError:
                flag2 = False
            if flag1 or flag2:
                if matcher.plugin_name == "poke":
                    raise IgnoredException("目前正在抢红包...")
            else:
                if matcher.plugin_name == "gold_redbag":
                    raise IgnoredException("目前没有红包...")
    except AttributeError:
        pass


@gold_redbag.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    global redbag_data, festive_redbag_data
    try:
        if time.time() - redbag_data[event.group_id]["time"] > 60:
            amount = (
                redbag_data[event.group_id]["amount"]
                - redbag_data[event.group_id]["open_amount"]
            )
            await return_gold(event.user_id, event.group_id, amount)
            await gold_redbag.send(
                f'{redbag_data[event.group_id]["nickname"]}的红包过时未开完，退还{amount}金币...'
            )
            redbag_data[event.group_id] = {}
        else:
            await gold_redbag.finish(
                f'目前 {redbag_data[event.group_id]["nickname"]} 的红包还没有开完噢，'
                f'还剩下 {len(redbag_data[event.group_id]["redbag"])} 个红包！'
                f'(或等待{str(60 - time.time() + redbag_data[event.group_id]["time"])[:2]}秒红包过时)'
            )
    except KeyError:
        pass
    msg = arg.extract_plain_text().strip()
    msg = msg.split()
    if len(msg) == 1:
        flag, amount = await check_gold(event.user_id, event.group_id, msg[0])
        if not flag:
            await gold_redbag.finish(amount)
        num = 5
    else:
        amount = msg[0]
        num = msg[1]
        if not is_number(num) or int(num) < 1:
            await gold_redbag.finish("红包个数给我输正确啊！", at_sender=True)
        flag, amount = await check_gold(event.user_id, event.group_id, amount)
        if not flag:
            await gold_redbag.finish(amount, at_sender=True)
        group_member_num = (await bot.get_group_info(group_id=event.group_id))[
            "member_count"
        ]
        num = int(num)
        if num > group_member_num:
            await gold_redbag.send("你发的红包数量也太多了，已经为你修改成与本群人数相同的红包数量...")
            num = group_member_num
    nickname = event.sender.card or event.sender.nickname
    flag, result = init_redbag(
        event.user_id, event.group_id, nickname, amount, num, int(bot.self_id)
    )
    if not flag:
        await gold_redbag.finish(result, at_sender=True)
    else:
        await gold_redbag.send(
            f"{nickname}发起了金币红包\n金额：{amount}\n数量：{num}\n"
            + image(
                b64=await generate_send_redbag_pic(
                    redbag_data[event.group_id]["user_id"]
                )
            )
        )
    logger.info(
        f"USER {event.user_id} GROUP {event.group_id} 塞入 {num} 个红包，共 {amount} 金币"
    )


@open_.handle()
async def _(event: GroupMessageEvent, arg: Message = CommandArg()):
    global redbag_data, festive_redbag_data
    msg = arg.extract_plain_text().strip()
    msg = (
        msg.replace("!", "")
        .replace("！", "")
        .replace(",", "")
        .replace("，", "")
        .replace(".", "")
        .replace("。", "")
    )
    if msg:
        if "红包" not in msg:
            return
    flag1 = True
    flag2 = True
    open_flag1 = True
    open_flag2 = True
    try:
        if festive_redbag_data[event.group_id]["user_id"]:
            if event.user_id in festive_redbag_data[event.group_id]["open_user"]:
                open_flag1 = False
    except KeyError:
        open_flag1 = False
        flag1 = False
    try:
        if redbag_data[event.group_id]["user_id"]:
            if event.user_id in redbag_data[event.group_id]["open_user"]:
                open_flag2 = False
    except KeyError:
        flag2 = False
    if not flag1 and not flag2:
        await open_.finish("目前没有红包可以开...", at_sender=True)
    if open_flag1 or open_flag2:
        try:
            await open_.send(
                image(b64=await get_redbag_img(event.user_id, event.group_id)),
                at_sender=True,
            )
        except KeyError:
            await open_.finish("真贪心，明明已经开过这个红包了的说...", at_sender=True)
    else:
        await open_.finish("真贪心，明明已经开过这个红包了的说...", at_sender=True)


@poke_.handle()
async def _poke_(event: PokeNotifyEvent):
    global redbag_data, festive_redbag_data
    if event.self_id == event.target_id:
        flag1 = True
        flag2 = True
        try:
            if event.user_id in festive_redbag_data[event.group_id]["open_user"]:
                flag1 = False
        except KeyError:
            flag1 = False
        try:
            if event.user_id in redbag_data[event.group_id]["open_user"]:
                flag2 = False
        except KeyError:
            flag2 = False
        if not flag1 and not flag2:
            return
        await poke_.send(
            image(b64=await get_redbag_img(event.user_id, event.group_id)),
            at_sender=True,
        )


@return_.handle()
async def _(event: GroupMessageEvent):
    global redbag_data
    try:
        if redbag_data[event.group_id]["user_id"] != event.user_id:
            await return_.finish("不是你的红包你退回什么！", at_sender=True)
        if time.time() - redbag_data[event.group_id]["time"] <= 60:
            await return_.finish(
                f'你的红包还没有过时，在 {str(60 - time.time() + redbag_data[event.group_id]["time"])[:2]} '
                f"秒后可以退回..",
                at_sender=True,
            )
        await return_gold(
            event.user_id,
            event.group_id,
            redbag_data[event.group_id]["amount"]
            - redbag_data[event.group_id]["open_amount"],
        )
        await return_.send(
            f"已成功退还了 "
            f"{redbag_data[event.group_id]['amount'] - redbag_data[event.group_id]['open_amount']} "
            f"金币",
            at_sender=True,
        )
        logger.info(
            f"USER {event.user_id} GROUP {event.group_id} 退回了"
            f"红包 {redbag_data[event.group_id]['amount'] - redbag_data[event.group_id]['open_amount']} 金币"
        )
        redbag_data[event.group_id] = {}
    except KeyError:
        await return_.finish("目前没有红包可以退回...", at_sender=True)


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
            try:
                scheduler.remove_job(f"festive_redbag_{g}")
                await end_festive_redbag(bot, g)
            except JobLookupError:
                pass
            init_redbag(
                int(bot.self_id), g, f"{NICKNAME}", amount, num, int(bot.self_id), 1
            )
            scheduler.add_job(
                end_festive_redbag,
                "date",
                run_date=(datetime.now() + timedelta(hours=24)).replace(microsecond=0),
                id=f"festive_redbag_{g}",
                args=[bot, g],
            )
            try:
                await bot.send_group_msg(
                    group_id=g,
                    message=f"{NICKNAME}发起了金币红包\n金额：{amount}\n数量：{num}\n"
                    + image(
                        b64=await generate_send_redbag_pic(int(bot.self_id), greetings)
                    ),
                )
            except ActionFailed:
                logger.warning(f"节日红包 GROUP {g} 发送失败..")
                pass


# 红包数据初始化
def init_redbag(
    user_id: int,
    group_id: int,
    nickname: str,
    amount: int,
    num: int,
    bot_self_id: int,
    mode: int = 0,
):
    global redbag_data, festive_redbag_data
    data = redbag_data if mode == 0 else festive_redbag_data
    if not data.get(group_id):
        data[group_id] = {}
    try:
        if data[group_id]["user_id"] and user_id != bot_self_id:
            return False, f'{data[group_id]["nickname"]}的红包还没抢完呢...'
    except KeyError:
        pass
    data[group_id]["user_id"] = user_id
    data[group_id]["nickname"] = nickname
    data[group_id]["amount"] = amount
    data[group_id]["num"] = num
    data[group_id]["open_amount"] = 0
    data[group_id]["time"] = time.time()
    data[group_id]["redbag"] = random_redbag(amount, num)
    data[group_id]["open_user"] = []
    if mode == 0:
        redbag_data = data
    else:
        festive_redbag_data = data
    return True, ""


# 随机红包排列
def random_redbag(amount: int, num: int) -> list:
    redbag_lst = []
    for _ in range(num - 1):
        tmp = int(amount / random.choice(range(3, num + 3)))
        redbag_lst.append(tmp)
        amount -= tmp
    redbag_lst.append(amount)
    return redbag_lst


# 返回开红包图片
async def get_redbag_img(user_id: int, group_id: int):
    global redbag_data, festive_redbag_data
    data = redbag_data
    mode = 0
    if festive_redbag_data.get(group_id):
        try:
            if user_id not in festive_redbag_data[group_id]["open_user"]:
                data = festive_redbag_data
                mode = 1
        except KeyError:
            pass
    amount, data = await open_redbag(user_id, group_id, data)
    text = (
        f"已领取"
        f'{data[group_id]["num"] - len(data[group_id]["redbag"])}'
        f'/{data[group_id]["num"]}个，'
        f'共{data[group_id]["open_amount"]}/{data[group_id]["amount"]}金币'
    )
    logger.info(
        f"USER {user_id} GROUP {group_id} 抢到了 {data[group_id]['user_id']} 的红包，获取了{amount}金币"
    )
    b64 = await generate_open_redbag_pic(
        data[group_id]["user_id"], data[group_id]["nickname"], amount, text
    )
    if data[group_id]["open_amount"] == data[group_id]["amount"]:
        data[group_id] = {}
    if mode == 0:
        redbag_data = data
    else:
        festive_redbag_data = data
    return b64


async def end_festive_redbag(bot: Bot, group_id: int):
    global festive_redbag_data
    message = (
        f"{NICKNAME}的节日红包过时了，一共开启了 "
        f"{festive_redbag_data[group_id]['num'] - len(festive_redbag_data[group_id]['redbag'])}"
        f" 个红包，共 {festive_redbag_data[group_id]['open_amount']} 金币"
    )
    await bot.send_group_msg(group_id=group_id, message=message)
    festive_redbag_data[group_id] = {}
