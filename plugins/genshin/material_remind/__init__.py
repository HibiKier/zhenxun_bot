from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent
from util.init_result import image

import time

material = on_command('今日素材', aliases={'今日材料', '今天素材', '今天材料'}, priority=5, block=True)
role_material = on_command('天赋材料', priority=5, block=True)


def get_today_material(name: str):
    # 返回今天的材料图片CQ码
    if name == '天赋材料':
        return image('天赋材料.png', "genshin/material/")
    week = time.strftime("%w")
    png_name = ''
    if week == "0":
        return "今天是周日，所有材料副本都开放了。"
    elif week in ["1", "4"]:
        png_name = f"{name}_周一周四.png"
    elif week in ["2", "5"]:
        png_name = f"{name}_周二周五.png"
    elif week in ["3", "6"]:
        png_name = f"{name}_周三周六.png"

    return image(png_name, "genshin/material/")


# @sv.on_fullmatch('开启原神每日素材提醒')
# async def open_remind(bot , ev):
#     gid = str(ev.group_id)
#     if not (gid in group_list):
#         group_list.append(gid)
#         save_group_list()
#     await bot.send(ev, "每日提醒已开启，每天8点会发送今日素材")
#
#
# @sv.on_fullmatch('关闭原神每日素材提醒')
# async def off_remind(bot , ev):
#     gid = str(ev.group_id)
#     if gid in group_list:
#         group_list.remove(gid)
#         save_group_list()
#     await bot.send(ev, "每日提醒已关闭")

@material.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    if time.strftime("%w") == "0":
        await material.send("今天是周日，所有材料副本都开放了。")
        return
    arms_material_CQ = get_today_material("武器突破材料")
    roles_material_CQ = get_today_material("角色天赋材料")
    await material.send(arms_material_CQ + roles_material_CQ)


@role_material.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await material.send(get_today_material("天赋材料"))

# @sv.scheduled_job('cron', hour='8')
# async def material_remind():
#     # 每日提醒
#     if time.strftime("%w") == "0":
#         # 如果今天是周日就不发了
#         return
#     bot = get_bot()
#     arms_material_CQ = get_today_material("武器突破材料")
#     roles_material_CQ = get_today_material("角色天赋材料")
#     for gid in group_list:
#         await bot.send_group_msg(group_id=int(gid), message=arms_material_CQ)
#         await bot.send_group_msg(group_id=int(gid), message=roles_material_CQ)
