

# async def open_remind(group: int, name: str) -> str:
#     _name = ""
#     if name == "zwa":
#         _name = "早晚安"
#     if name == "dz":
#         _name = "地震播报"
#     if name == "hy":
#         _name = "群欢迎"
#     if name == "kxcz":
#         _name = "开箱重置提醒"
#     if name == "gb":
#         _name = "广播"
#     if await GroupRemind.get_status(group, name):
#         return f"该群已经开启过 {_name} 通知，请勿重复开启！"
#     if await GroupRemind.set_status(group, name, True):
#         return f"成功开启 {_name} 通知！0v0"
#     else:
#         return f"开启 {_name} 通知失败了..."
#
#
# async def close_remind(group: int, name: str) -> str:
#     _name = ""
#     if name == "zwa":
#         _name = "早晚安"
#     if name == "dz":
#         _name = "地震播报"
#     if name == "hy":
#         _name = "群欢迎"
#     if name == "kxcz":
#         _name = "开箱重置提醒"
#     if name == "gb":
#         _name = "广播"
#     if not await GroupRemind.get_status(group, name):
#         return f"该群已经取消过 {_name} 通知，请勿重复取消！"
#     if await GroupRemind.set_status(group, name, False):
#         return f"成功关闭 {_name} 通知！0v0"
#     else:
#         return f"关闭 {_name} 通知失败了..."


# cmd_list = ['总开关', '签到', '发送图片', '色图', '黑白草图', 'coser', '鸡汤/语录', '骂我', '开箱', '鲁迅说', '假消息', '商店系统',
#             '操作图片', '查询皮肤', '天气', '疫情', '识番', '搜番', '点歌', 'pixiv', 'rss', '方舟一井', '查干员', '骰子娘', '原神一井']
#
#
# def check_group_switch_json(group_id):
#     if not os.path.exists(DATA_PATH + f'rule/group_switch/'):
#         os.mkdir(DATA_PATH + f'rule/group_switch/')
#     if not os.path.exists(DATA_PATH + f'rule/group_switch/{group_id}.json'):
#         with open(DATA_PATH + f'rule/group_switch/{group_id}.json', 'w', encoding='utf8') as f:
#             data = {}
#             for cmd in cmd_list:
#                 data[cmd] = True
#             f.write(json.dumps(data, ensure_ascii=False))
#     else:
#         with open(DATA_PATH + f'rule/group_switch/{group_id}.json', 'r', encoding='utf8') as f:
#             try:
#                 data = json.load(f)
#             except ValueError:
#                 data = {}
#             if len(data.keys()) - 1 != len(cmd_list):
#                 for cmd in cmd_list:
#                     if cmd not in data.keys():
#                         data[cmd] = True
#                 with open(DATA_PATH + f'rule/group_switch/{group_id}.json', 'w', encoding='utf8') as wf:
#                     wf.write(json.dumps(data, ensure_ascii=False))
#     reload(data)
#     for file in os.listdir(DATA_PATH + 'group_help'):
#         os.remove(DATA_PATH + f'group_help/{file}')


def reload(data):
    static_group_dict = data
