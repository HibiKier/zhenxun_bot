from .group_user_checkin import (
    group_user_check_in,
    group_user_check,
    group_impression_rank,
    impression_rank,
    check_in_all
)
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message
from nonebot.adapters.onebot.v11.permission import GROUP
from utils.message_builder import image
from nonebot import on_command
from utils.utils import scheduler
from nonebot.params import CommandArg
from pathlib import Path
from configs.path_config import DATA_PATH
from services.log import logger
from .utils import clear_sign_data_pic
from utils.utils import is_number

try:
    import ujson as json
except ModuleNotFoundError:
    import json

__zx_plugin_name__ = "签到"
__plugin_usage__ = """
usage：
    每日签到
    会影响色图概率和开箱次数，以及签到的随机道具获取
    指令：
        签到 ?[all]: all代表签到所有群
        我的签到
        好感度排行
        好感度总排行
    * 签到时有 3% 概率 * 2 *
""".strip()
__plugin_des__ = "每日签到，证明你在这里"
__plugin_cmd__ = ["签到 ?[all]", "我的签到", "好感度排行", "好感度总排行"]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["签到"],
}
__plugin_cd_limit__ = {}
__plugin_configs__ = {
    "MAX_SIGN_GOLD": {"value": 200, "help": "签到好感度加成额外获得的最大金币数", "default_value": 200},
    "SIGN_CARD1_PROB": {"value": 0.2, "help": "签到好感度双倍加持卡Ⅰ掉落概率", "default_value": 0.2},
    "SIGN_CARD2_PROB": {
        "value": 0.09,
        "help": "签到好感度双倍加持卡Ⅱ掉落概率",
        "default_value": 0.09,
    },
    "SIGN_CARD3_PROB": {
        "value": 0.05,
        "help": "签到好感度双倍加持卡Ⅲ掉落概率",
        "default_value": 0.05,
    },
}


_file = Path(f"{DATA_PATH}/not_show_sign_rank_user.json")
try:
    data = json.load(open(_file, "r", encoding="utf8"))
except (FileNotFoundError, ValueError, TypeError):
    data = {"0": []}


sign = on_command("签到", priority=5, permission=GROUP, block=True)
my_sign = on_command(
    cmd="我的签到", aliases={"好感度"}, priority=5, permission=GROUP, block=True
)
sign_rank = on_command(
    cmd="积分排行",
    aliases={"好感度排行", "签到排行", "积分排行", "好感排行", "好感度排名，签到排名，积分排名"},
    priority=5,
    permission=GROUP,
    block=True,
)
total_sign_rank = on_command(
    "签到总排行", aliases={"好感度总排行", "好感度总榜", "签到总榜"}, priority=5, block=True
)


@sign.handle()
async def _(event: GroupMessageEvent, arg: Message = CommandArg()):
    nickname = event.sender.card or event.sender.nickname
    await sign.send(
        await group_user_check_in(nickname, event.user_id, event.group_id),
        at_sender=True,
    )
    if arg.extract_plain_text().strip() == "all":
        await check_in_all(nickname, event.user_id)


@my_sign.handle()
async def _(event: GroupMessageEvent):
    nickname = event.sender.card or event.sender.nickname
    await my_sign.send(
        await group_user_check(nickname, event.user_id, event.group_id),
        at_sender=True,
    )


@sign_rank.handle()
async def _(event: GroupMessageEvent, arg: Message = CommandArg()):
    num = arg.extract_plain_text().strip()
    if is_number(num) and 51 > int(num) > 10:
        num = int(num)
    else:
        num = 10
    _image = await group_impression_rank(event.group_id, num)
    if _image:
        await sign_rank.send(image(b64=_image.pic2bs4()))


@total_sign_rank.handle()
async def _(event: GroupMessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    if not msg:
        await total_sign_rank.send("请稍等..正在整理数据...")
        await total_sign_rank.send(image(b64=await impression_rank(0, data)))
    elif msg in ["屏蔽我"]:
        if event.user_id in data["0"]:
            await total_sign_rank.finish("您已经在屏蔽名单中了，请勿重复添加！", at_sender=True)
        data["0"].append(event.user_id)
        await total_sign_rank.send("设置成功，您不会出现在签到总榜中！", at_sender=True)
    elif msg in ["显示我"]:
        if event.user_id not in data["0"]:
            await total_sign_rank.finish("您不在屏蔽名单中！", at_sender=True)
        data["0"].remove(event.user_id)
        await total_sign_rank.send("设置成功，签到总榜将会显示您的头像名称以及好感度！", at_sender=True)
    with open(_file, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


@scheduler.scheduled_job(
    "interval",
    hours=1,
)
async def _():
    try:
        clear_sign_data_pic()
        logger.info("清理日常签到图片数据数据完成....")
    except Exception as e:
        logger.error(f"清理日常签到图片数据数据失败..{type(e)}: {e}")
