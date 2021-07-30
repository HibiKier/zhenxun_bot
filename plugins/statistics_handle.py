from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, MessageEvent
from models.group_info import GroupInfo
from nonebot.typing import T_State
from pathlib import Path
from configs.path_config import DATA_PATH, TTF_PATH
import matplotlib.pyplot as plt
from utils.utils import get_message_text
from utils.image_utils import fig2b64
from utils.message_builder import image
from configs.config import plugins2info_dict
from matplotlib.font_manager import FontProperties

plt.rcParams["font.family"] = ["SimHei", "FangSong", "KaiTi"]
plt.rcParams["font.sans-serif"] = ["SimHei", "FangSong", "KaiTi"]
plt.rcParams["axes.unicode_minus"] = False

font = FontProperties(fname=f"{TTF_PATH}/yz.ttf", size=10)

try:
    import ujson as json
except ModuleNotFoundError:
    import json

__plugin_name__ = "功能调用统计"
__plugin_usage__ = "用法： 无"

statistics = on_command(
    "功能调用统计",
    aliases={
        "日功能调用统计",
        "周功能调用统计",
        "月功能调用统计",
        "我的功能调用统计",
        "我的日功能调用统计",
        "我的周功能调用统计",
        "我的月功能调用统计",
    },
    priority=5,
    block=True,
)


statistics_group_file = Path(f"{DATA_PATH}/_prefix_count.json")
statistics_user_file = Path(f"{DATA_PATH}/_prefix_user_count.json")


@statistics.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json())
    if state["_prefix"]["raw_command"][:2] == "我的":
        itype = "user"
        key = str(event.user_id)
        state["_prefix"]["raw_command"] = state["_prefix"]["raw_command"][2:]
        if not statistics_user_file.exists():
            await statistics.finish("统计文件不存在...", at_sender=True)
    else:
        if not isinstance(event, GroupMessageEvent):
            await statistics.finish("请在群内调用此功能...")
        itype = "group"
        key = str(event.group_id)
        if not statistics_group_file.exists():
            await statistics.finish("统计文件不存在...", at_sender=True)
    plugin = ""
    if state["_prefix"]["raw_command"][0] == "日":
        arg = "day_statistics"
    elif state["_prefix"]["raw_command"][0] == "周":
        arg = "week_statistics"
    elif state["_prefix"]["raw_command"][0] == "月":
        arg = "month_statistics"
    else:
        arg = "total_statistics"
    if msg:
        for x in plugins2info_dict.keys():
            if msg in plugins2info_dict[x]["cmd"]:
                plugin = plugins2info_dict[x]["cmd"][0]
                break
        else:
            if arg not in ["day_statistics", "total_statistics"]:
                await statistics.finish("未找到此功能的调用...", at_sender=True)
    if itype == "group":
        data: dict = json.load(open(statistics_group_file, "r", encoding="utf8"))
        if not data[arg].get(str(event.group_id)):
            await statistics.finish("该群统计数据不存在...", at_sender=True)
    else:
        data: dict = json.load(open(statistics_user_file, "r", encoding="utf8"))
        if not data[arg].get(str(event.user_id)):
            await statistics.finish("该用户统计数据不存在...", at_sender=True)
    day_index = data["day_index"]
    data = data[arg][key]
    if itype == "group":
        name = await GroupInfo.get_group_info(event.group_id)
        name = name.group_name if name else str(event.group_id)
    else:
        name = event.sender.card if event.sender.card else event.sender.nickname
    img = generate_statistics_img(data, arg, name, plugin, day_index)
    await statistics.send(image(b64=img))
    plt.cla()


def generate_statistics_img(
    data: dict, arg: str, name: str, plugin: str, day_index: int
):
    if arg == "day_statistics":
        init_bar_graph(data, f"{name} 日功能调用统计")
    elif arg == "week_statistics":
        if plugin:
            current_week = day_index % 7
            week_lst = []
            if current_week == 0:
                week_lst = [1, 2, 3, 4, 5, 6, 7]
            else:
                for i in range(current_week + 1, 7):
                    week_lst.append(str(i))
                for i in range(current_week + 1):
                    week_lst.append(str(i))
            count = []
            for i in range(7):
                if int(week_lst[i]) == 7:
                    try:
                        count.append(data[str(0)][plugin])
                    except KeyError:
                        count.append(0)
                else:
                    try:
                        count.append(data[str(week_lst[i])][plugin])
                    except KeyError:
                        count.append(0)
            week_lst = ["7" if i == "0" else i for i in week_lst]
            plt.plot(week_lst, count)
            plt.title(f"{name} 周 {plugin} 功能调用统计【为7天统计】", FontProperties=font)
        else:
            init_bar_graph(update_data(data), f"{name} 周功能调用统计【为7天统计】")
    elif arg == "month_statistics":
        if plugin:
            day_index = day_index % 30
            day_lst = []
            for i in range(day_index + 1, 30):
                day_lst.append(i)
            for i in range(day_index + 1):
                day_lst.append(i)
            count = [data[str(day_lst[i])][plugin] for i in range(30)]
            day_lst = [str(x + 1) for x in day_lst]
            plt.title(f"{name} 月 {plugin} 功能调用统计【为30天统计】", FontProperties=font)
            plt.plot(day_lst, count)
        else:
            init_bar_graph(update_data(data), f"{name} 月功能调用统计【为30天统计】")
    elif arg == "total_statistics":
        init_bar_graph(data, f"{name} 功能调用统计")

    return fig2b64(plt)


def init_bar_graph(data: dict, title: str, ha: str = "left", va: str = "center"):
    plt.tick_params(axis="y", labelsize=7)
    tmp_x = list(data.keys())
    tmp_y = list(data.values())
    x = [tmp_x[i] for i in range(len(tmp_y)) if tmp_y[i]]
    y = [tmp_y[i] for i in range(len(tmp_y)) if tmp_y[i]]
    plt.barh(x, y)
    plt.title(f"{title}", FontProperties=font)
    for y, x in zip(y, x):
        plt.text(y, x, s=str(y), ha=ha, va=va, fontsize=8)


def update_data(data: dict):
    tmp_dict = {}
    for day in data.keys():
        for plugin_name in data[day].keys():
            # print(f'{day}：{plugin_name} = {data[day][plugin_name]}')
            if data[day][plugin_name] is not None:
                if tmp_dict.get(plugin_name) is None:
                    tmp_dict[plugin_name] = 1
                else:
                    tmp_dict[plugin_name] += data[day][plugin_name]
    return tmp_dict
