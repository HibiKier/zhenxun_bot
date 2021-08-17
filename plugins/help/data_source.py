from utils.image_utils import CreateImg
from configs.path_config import IMAGE_PATH, DATA_PATH
from pathlib import Path
from .config import *
from configs.config import (
    INITIAL_OPEN_CASE_COUNT,
    INITIAL_SETU_PROBABILITY,
    ADMIN_DEFAULT_AUTH,
)
from configs.config import plugins2info_dict, NICKNAME
from utils.static_data import group_manager
import nonebot


width = 1600
e_height = 0
u_height = 950
o_height = 1500
# f_height =


def create_help_img():
    help_img_file = Path(IMAGE_PATH) / 'help.png'
    if help_img_file.exists():
        help_img_file.unlink()
    h = (
        100
        + len(utility_help) * 24
        + len(entertainment_help) * 24
        + len(other_help) * 24
    ) * 2
    A = CreateImg(width, h - 200, font_size=24)
    e = CreateImg(width, len(entertainment_help) * 42, font_size=24)
    rst = ""
    i = 0
    for cmd in entertainment_help:
        rst += f"{i + 1}.{entertainment_help[cmd]}\n"
        i += 1
    e.text((10, 10), "娱乐功能：")
    e.text((40, 40), rst)
    u = CreateImg(width, len(utility_help) * 40 + 50, font_size=24, color="black")
    rst = ""
    i = 0
    for cmd in utility_help:
        rst += f"{i + 1}.{utility_help[cmd]}\n"
        i += 1
    u.text((10, 10), "实用功能：", fill=(255, 255, 255))
    u.text((40, 40), rst, fill=(255, 255, 255))
    o = CreateImg(width, len(other_help) * 40, font_size=24)
    rst = ""
    i = 0
    for i in range(len(other_help)):
        rst += f"{i + 1}.{other_help[i]}\n"
        i += 1
    o.text((10, 10), "其他功能：")
    o.text((40, 40), rst)
    A.paste(e, (0, 0))
    A.paste(u, (0, u_height))
    A.paste(o, (0, o_height))
    A.text(
        (10, h * 0.68),
        f"大部分交互功能可以通过输入‘取消’，‘算了’来取消当前交互\n对{NICKNAME}说 “{NICKNAME}帮助 指令名” 获取对应详细帮助\n"
        "可以通过 “滴滴滴- [消息]” 联系管理员（有趣的想法尽管来吧！<还有Bug和建议>）"
        "\n[群管理员请看 管理员帮助（群主与管理员自带 5 级权限）]\n\n"
        f"\t「如果{NICKNAME}回复了一些不符合人设的话，那是因为每日白嫖的图灵次数已用完，使用的是备用接口【QAQ】」",
    )

    A.save(IMAGE_PATH + "help.png")


def create_group_help_img(group_id: int):
    group_id = str(group_id)
    h = (
        100
        + len(utility_help) * 24
        + len(entertainment_help) * 24
        + len(other_help) * 24
    ) * 2
    A = CreateImg(width, h - 200, font_size=24)
    u = CreateImg(width, len(utility_help) * 40, font_size=24, color="black")
    o = CreateImg(width, len(other_help) * 40, font_size=24)
    e = CreateImg(width, len(entertainment_help) * 42, font_size=24)
    rst = ""
    i = 1
    for cmd in entertainment_help.keys():
        flag, dfg = parse_cmd(cmd, group_id)
        if dfg:
            cmd = rcmd(dfg)
        rst += f"【{flag}】{i}.{entertainment_help[cmd]}\n"
        i += 1
    e.text((10, 10), "娱乐功能：")
    e.text((40, 40), rst)

    rst = ""
    i = 1
    for cmd in utility_help.keys():
        flag, dfg = parse_cmd(cmd, group_id)
        rst += f"【{flag}】{i}.{utility_help[cmd]}\n"
        i += 1
    u.text((10, 10), "实用功能：", fill=(255, 255, 255))
    u.text((40, 40), rst, fill=(255, 255, 255))

    rst = ""
    for i in range(len(other_help)):
        rst += f"{i + 1}.{other_help[i]}\n"
    o.text((10, 10), "其他功能：")
    o.text((40, 40), rst)

    A.paste(e, (0, 0))
    A.paste(u, (0, u_height))
    A.paste(o, (0, o_height))
    # A.text((width, 10), f'总开关【{"√" if data["总开关"] else "×"}】')
    A.text(
        (10, h * 0.68),
        f"大部分交互功能可以通过输入‘取消’，‘算了’来取消当前交互\n对{NICKNAME}说 “{NICKNAME}帮助 指令名” 获取对应详细帮助\n"
        "可以通过 “滴滴滴- [消息]” 联系管理员（有趣的想法尽管来吧！<还有Bug和建议>）"
        f"\n[群管理员请看 管理员帮助（群主与管理员自带 {ADMIN_DEFAULT_AUTH} 级权限）]",
    )
    A.text(
        (10, h * 0.77),
        f"【注】「色图概率：好感度 + {int(INITIAL_SETU_PROBABILITY*100)}%\n"
        f"\t\t每 3 点好感度 + 1次开箱，初始 {INITIAL_OPEN_CASE_COUNT} 次\n"
        f"\t\t开启/关闭功能只需输入‘开启/关闭 指令名’（每个功能的第一个指令）」\n"
        f"\t\t示例：开启签到\n"
        f"\t\t可以通过管理员开关自动发送消息(早晚安等)\n"
        f"\t\t^请查看管理员帮助^\n\n"
        f"\t「如果{NICKNAME}回复了一些不符合人设的话，那是因为每日白嫖的图灵次数已用完，使用的是备用接口【QAQ】」",
    )
    A.save(DATA_PATH + f"group_help/{group_id}.png")


def parse_cmd(cmd, group_id):
    flag = "√"
    dfg = None
    if cmd.find("draw_card") != -1:
        lst = cmd.split("_")
        cmd = lst[0] + "_" + lst[1]
        dfg = lst[-1]
    elif cmd == "pixiv_r":
        cmd = "pixiv"
        dfg = "r"
    elif cmd == "pixiv_s":
        cmd = "pixiv"
        dfg = "s"
    if not group_manager.get_plugin_status(cmd, group_id):
        flag = "×"
    if cmd in ["bt", "reimu", "nickname"]:
        flag = "- "
    return flag, dfg


def rcmd(dfg):
    if dfg in [
        "prts",
        "genshin",
        "pretty",
        "guardian",
        "pcr",
        "azur",
        "onmyoji",
        "fgo",
    ]:
        return "draw_card_" + dfg
    if dfg == "r":
        return "pixiv_r"
    if dfg == "s":
        return "pixiv_s"


def get_plugin_help(msg: str) -> str:
    plugin = None
    for p in plugins2info_dict.keys():
        if msg in plugins2info_dict[p]["cmd"]:
            plugin = nonebot.plugin.get_plugin(p)
            break
    if plugin:
        result = plugin.module.__getattribute__("__plugin_usage__")
        return result
    else:
        return "没有此功能的帮助信息..."
