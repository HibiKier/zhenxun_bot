# coding=utf-8
from nonebot import on_command
from nonebot.typing import T_State

from services.log import logger
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    PrivateMessageEvent,
    GROUP,
)
from os.path import join
from configs.config import NICKNAME
from .Life import Life
from .PicClass import *
import traceback
import random

__zx_plugin_name__ = "人生重开 - lifeRestart"
__plugin_usage__ = """
usage：
    remake/人生重来/人生重开/人生重启
    即可再来一段人生
""".strip()
__plugin_des__ = "人生重来模拟器"
__plugin_cmd__ = [
    "remake",
    "人生重来",
    "人生重开",
    "人生重启",
]
__plugin_type__ = ("群内小游戏",)
__plugin_version__ = 0.2
__plugin_author__ = "AkashiCoin"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["remake", "人生重来", "人生重开", "人生重启"],
}
__plugin_block_limit__ = {"rst": "你的垃圾人生正在重开，请稍等..."}

remake = on_command(
    "remake", aliases={"人生重开", "人生重来", "人生重启"}, permission=GROUP, priority=5, block=True
)


def genp(prop):
    ps = []
    # for _ in range(4):
    #     ps.append(min(prop, 8))
    #     prop -= ps[-1]
    tmp = prop
    while True:
        for i in range(0, 4):
            if i == 3:
                ps.append(tmp)
            else:
                if tmp >= 10:
                    ps.append(random.randint(0, 10))
                else:
                    ps.append(random.randint(0, tmp))
                tmp -= ps[-1]
        if ps[3] < 10:
            break
        else:
            tmp = prop
            ps.clear()
    return {"CHR": ps[0], "INT": ps[1], "STR": ps[2], "MNY": ps[3]}


@remake.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    pic_list = []
    mes_list = []

    Life.load(join(FILE_PATH, "data"))
    while True:
        life = Life()
        life.setErrorHandler(lambda e: traceback.print_exc())
        life.setTalentHandler(lambda ts: random.choice(ts).id)
        life.setPropertyhandler(genp)
        flag = life.choose()
        if flag:
            break

    name = event.sender.card if event.sender.card else event.sender.nickname
    choice = 0
    person = name + "本次重生的基本信息如下：\n\n【你的天赋】\n"
    for t in life.talent.talents:
        choice = choice + 1
        person = person + str(choice) + "、天赋：【" + t.name + "】" + " 效果:" + t.desc + "\n"

    person = person + "\n【基础属性】\n"
    person = person + "   美貌值:" + str(life.property.CHR) + "  "
    person = person + "智力值:" + str(life.property.INT) + "  "
    person = person + "体质值:" + str(life.property.STR) + "  "
    person = person + "财富值:" + str(life.property.MNY) + "  "
    pic_list.append("这是" + name + "本次轮回的基础属性和天赋:")
    pic_list.append(ImgText(person).draw_text())

    await bot.send(event, "你的命运正在重启....", at_sender=True)
    logger.info(
        f"USER {event.user_id} GROUP {event.group_id if not isinstance(event, PrivateMessageEvent) else ''} "
        f"感觉人生太过垃圾，remake了"
    )
    res = life.run()  # 命运之轮开始转动
    mes = "\n".join("\n".join(x) for x in res)
    pic_list.append("这是" + name + "本次轮回的生平:")
    pic_list.append(ImgText(mes).draw_text())

    sums = life.property.gensummary()  # 你的命运之轮到头了
    pic_list.append("这是" + name + "本次轮回的评价:")
    pic_list.append(ImgText(sums).draw_text())

    for img in pic_list:
        data = {
            "type": "node",
            "data": {"name": f"{NICKNAME}", "uin": f"{bot.self_id}", "content": img},
        }
        mes_list.append(data)

    await bot.send_group_forward_msg(group_id=event.group_id, messages=mes_list)
