from util.img_utils import CreateImg
from configs.path_config import IMAGE_PATH, DATA_PATH
import ujson as json
import os
from .config import *
from nonebot import require

export = require("nonebot_plugin_manager")

width = 1200
e_height = 0
u_height = 700
o_height = 1250
# f_height =


def create_help_img():
    if os.path.exists(IMAGE_PATH + 'help.png'):
        os.remove(IMAGE_PATH + 'help.png')
    h = (100 + len(utility_help) * 24 + len(entertainment_help) * 24 + len(other_help) * 24) * 2
    A = CreateImg(width, h - 200, font_size=24)
    e = CreateImg(width, len(entertainment_help) * 42, font_size=24)
    rst = ''
    i = 0
    for cmd in entertainment_help:
        rst += f'{i + 1}.{entertainment_help[cmd]}\n'
        i += 1
    e.text((10, 10), '娱乐功能：')
    e.text((40, 40), rst)
    u = CreateImg(width, len(utility_help) * 40 + 50, font_size=24, color='black')
    rst = ''
    i = 0
    for cmd in utility_help:
        rst += f'{i + 1}.{utility_help[cmd]}\n'
        i += 1
    u.text((10, 10), '实用功能：', fill=(255, 255, 255))
    u.text((40, 40), rst, fill=(255, 255, 255))
    o = CreateImg(width, len(other_help) * 40, font_size=24)
    rst = ''
    i = 0
    for i in range(len(other_help)):
        rst += f'{i + 1}.{other_help[i]}\n'
        i += 1
    o.text((10, 10), '其他功能：')
    o.text((40, 40), rst)
    A.paste(e, (0, 0))
    A.paste(u, (0, u_height))
    A.paste(o, (0, o_height))
    A.text((10, h * 0.72), '大部分交互功能可以通过输入‘取消’，‘算了’来取消当前交互\n对我说 “指令名 帮助” 获取对应详细帮助\n'
                           '可以通过 “滴滴滴- 后接内容” 联系管理员（有趣的想法尽管来吧！<还有Bug和建议>）\n[群管理员请看 管理员帮助（群主与管理员自带 5 级权限）]')
    A.text((10, h * 0.79), f"【注】「色图概率：好感度 + 70%\n"
                           f"\t\t每 3 点好感度 + 1次开箱，初始 20 次\n"
                           f"\t\t开启/关闭功能只需输入‘开启/关闭 指令名’（每个功能的第一个指令）」\n"
                           f"\t\t示例：开启签到")
    A.save(IMAGE_PATH + 'help.png')


def create_group_help_img(group_id: int):
    group_id = str(group_id)
    try:
        with open(DATA_PATH + 'manager/plugin_list.json', 'r', encoding='utf8') as f:
            plugin_list = json.load(f)
    except (ValueError, FileNotFoundError):
        pass
    h = (100 + len(utility_help) * 24 + len(entertainment_help) * 24 + len(other_help) * 24) * 2
    A = CreateImg(1200, h - 200, font_size=24)
    u = CreateImg(1200, len(utility_help) * 40, font_size=24, color='black')
    o = CreateImg(1200, len(other_help) * 40, font_size=24)
    e = CreateImg(width, len(entertainment_help) * 42, font_size=24)
    rst = ''
    i = 1
    # print(plugin_list)
    for cmd in entertainment_help.keys():
        # dfg = '_'
        # if cmd == 'draw_card_p':
        #     cmd = 'draw_card'
        #     dfg = 'p'
        # elif cmd == 'draw_card_g':
        #     cmd = 'draw_card'
        #     dfg = 'g'
        # flag = '√'
        # if group_id in plugin_list[cmd]:
        #     if not plugin_list[cmd][group_id]:
        #         flag = '×'
        # if cmd in ['nickname']:
        #     flag = '-'
        flag, dfg = parse_cmd(cmd, group_id, plugin_list)
        if dfg:
            cmd = rcmd(dfg)
        # if dfg == 'p':
        #     cmd = 'draw_card_p'
        # elif dfg == 'g':
        #     cmd = 'draw_card_g'
        rst += f'【{flag}】{i}.{entertainment_help[cmd]}\n'
        i += 1
    e.text((10, 10), '娱乐功能：')
    e.text((40, 40), rst)

    rst = ''
    i = 1
    for cmd in utility_help.keys():
        # flag = '√'
        # if group_id in plugin_list[cmd]:
        #     if not plugin_list[cmd][group_id]:
        #         flag = '×'
        # if cmd in ['bt', 'reimu']:
        #     flag = '-'
        flag, dfg = parse_cmd(cmd, group_id, plugin_list)
        rst += f'【{flag}】{i}.{utility_help[cmd]}\n'
        i += 1
    u.text((10, 10), '实用功能：', fill=(255, 255, 255))
    u.text((40, 40), rst, fill=(255, 255, 255))

    rst = ''
    for i in range(len(other_help)):
        rst += f'{i + 1}.{other_help[i]}\n'
    o.text((10, 10), '其他功能：')
    o.text((40, 40), rst)

    A.paste(e, (0, 0))
    A.paste(u, (0, u_height))
    A.paste(o, (0, o_height))
    # A.text((width, 10), f'总开关【{"√" if data["总开关"] else "×"}】')
    A.text((10, h * 0.72), '大部分交互功能可以通过输入‘取消’，‘算了’来取消当前交互\n对我说 “指令名 帮助” 获取对应详细帮助\n'
                           '可以通过 “滴滴滴- 后接内容” 联系管理员（有趣的想法尽管来吧！<还有Bug和建议>）'
                           '\n[群管理员请看 管理员帮助（群主与管理员自带 5 级权限）]')
    A.text((10, h * 0.79), f"【注】「色图概率：好感度 + 70%\n"
                           f"\t\t每 3 点好感度 + 1次开箱，初始 20 次\n"
                           f"\t\t开启/关闭功能只需输入‘开启/关闭 指令名’（每个功能的第一个指令）」\n"
                           f"\t\t示例：开启签到\n"
                           f"\t\t可以通过管理员开关自动发送消息(早晚安等)\n"
                           f"\t\t^请查看管理员帮助^")
    A.save(DATA_PATH + f'group_help/{group_id}.png')


def parse_cmd(cmd, group_id, plugin_list):
    flag = '√'
    dfg = None
    if cmd == 'draw_card_p':
        cmd = 'draw_card'
        dfg = 'p'
    elif cmd == 'draw_card_g':
        cmd = 'draw_card'
        dfg = 'g'
    elif cmd == 'draw_card_h':
        cmd = 'draw_card'
        dfg = 'h'
    elif cmd == 'pixiv_r':
        cmd = 'pixiv'
        dfg = 'r'
    elif cmd == 'pixiv_s':
        cmd = 'pixiv'
        dfg = 's'
    if group_id in plugin_list[cmd]:
        if not plugin_list[cmd][group_id]:
            flag = '×'
    if cmd in ['bt', 'reimu', 'nickname']:
        flag = '- '
    return flag, dfg


def rcmd(dfg):
    if dfg == 'p':
        return 'draw_card_p'
    if dfg == 'g':
        return 'draw_card_g'
    if dfg == 'g':
        return 'draw_card_h'
    if dfg == 'r':
        return 'pixiv_r'
    if dfg == 's':
        return 'pixiv_s'



