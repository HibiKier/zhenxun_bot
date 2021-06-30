from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, GROUP
from models.group_info import GroupInfo
from nonebot.typing import T_State
from pathlib import Path
from configs.path_config import DATA_PATH, TTF_PATH
import matplotlib.pyplot as plt
from utils.utils import get_message_text
from utils.img_utils import fig2b64
from utils.init_result import image
from configs.config import plugins2info_dict
from matplotlib.font_manager import FontProperties

plt.rcParams['font.family'] = ['SimHei', 'FangSong', 'KaiTi']
plt.rcParams['font.sans-serif'] = ['SimHei', 'FangSong', 'KaiTi']
plt.rcParams['axes.unicode_minus'] = False

font = FontProperties(fname=f'{TTF_PATH}/yz.ttf', size=10)

try:
    import ujson as json
except ModuleNotFoundError:
    import json

__plugin_name__ = '功能调用统计'
__plugin_usage__ = '用法： 无'

statistics = on_command("功能调用统计", aliases={'日功能调用统计', '周功能调用统计', '月功能调用统计'}, permission=GROUP, priority=5, block=True)

statistics_file = Path(f'{DATA_PATH}/_prefix_count.json')


@statistics.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = get_message_text(event.json())
    plugin = ''
    if not statistics_file.exists():
        await statistics.finish('统计文件不存在...', at_sender=True)
    if state["_prefix"]["raw_command"][0] == '日':
        arg = 'day_statistics'
    elif state["_prefix"]["raw_command"][0] == '周':
        arg = 'week_statistics'
    elif state["_prefix"]["raw_command"][0] == '月':
        arg = 'month_statistics'
    else:
        arg = 'total_statistics'
    if msg:
        for key in plugins2info_dict.keys():
            if msg in plugins2info_dict[key]['cmd']:
                plugin = plugins2info_dict[key]['cmd'][0]
                break
        else:
            if arg not in ['day_statistics', 'total_statistics']:
                await statistics.finish('未找到此功能的调用...', at_sender=True)
    data: dict = json.load(open(statistics_file, 'r', encoding='utf8'))
    if not data[arg].get(str(event.group_id)):
        await statistics.finish('该群统计数据不存在...', at_sender=True)
    day_index = data['day_index']
    data = data[arg][str(event.group_id)]
    group_name = await GroupInfo.get_group_info(event.group_id)
    group_name = group_name.group_name if group_name else str(event.group_id)
    img = generate_statistics_img(data, arg, group_name, plugin, day_index)
    await statistics.send(image(b64=img))
    plt.cla()


def generate_statistics_img(data: dict, arg: str, group_name: str, plugin: str, day_index: int):
    if arg == 'day_statistics':
        init_bar_graph(data, f'{group_name} 日功能调用统计')
    elif arg == 'week_statistics':
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
                    count.append(data[str(0)][plugin])
                else:
                    count.append(data[str(week_lst[i])][plugin])
            week_lst = ['7' if i == '0' else i for i in week_lst]
            plt.plot(week_lst, count)
            plt.title(f'{group_name} 周 {plugin} 功能调用统计【为7天统计】', FontProperties=font)
        else:
            init_bar_graph(update_data(data), f'{group_name} 周功能调用统计【为7天统计】')
    elif arg == 'month_statistics':
        if plugin:
            day_index = day_index % 30
            day_lst = []
            for i in range(day_index + 1, 30):
                day_lst.append(i)
            for i in range(day_index + 1):
                day_lst.append(i)
            count = [data[str(day_lst[i])][plugin] for i in range(30)]
            day_lst = [str(x + 1) for x in day_lst]
            plt.title(f'{group_name} 月 {plugin} 功能调用统计【为30天统计】', FontProperties=font)
            plt.plot(day_lst, count)
        else:
            init_bar_graph(update_data(data), f'{group_name} 月功能调用统计【为30天统计】')
    elif arg == 'total_statistics':
        init_bar_graph(data, f'{group_name} 功能调用统计')

    return fig2b64(plt)


def init_bar_graph(data: dict, title: str, ha: str = 'left', va: str = 'center'):
    plt.tick_params(axis='y', labelsize=7)
    tmp_x = list(data.keys())
    tmp_y = list(data.values())
    x = [tmp_x[i] for i in range(len(tmp_y)) if tmp_y[i]]
    y = [tmp_y[i] for i in range(len(tmp_y)) if tmp_y[i]]
    plt.barh(x, y)
    plt.title(f'{title}', FontProperties=font)
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
