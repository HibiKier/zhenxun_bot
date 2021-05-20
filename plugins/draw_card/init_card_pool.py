from typing import Any


def init_game_pool(game: str, data: dict, Operator: Any):
    tmp_lst = []
    if game == 'prts':
        for key in data.keys():
            limited = False
            recruit_only = False
            event_only = False
            if '限定寻访' in data[key]['获取途径']:
                limited = True
            if len(data[key]['获取途径']) == 1 and data[key]['获取途径'][0] == '公开招募':
                recruit_only = True
            if '活动获取' in data[key]['获取途径']:
                event_only = True
            if key.find('阿米娅') != -1:
                continue
            tmp_lst.append(Operator(name=key, star=int(data[key]['星级']),
                                    limited=limited, recruit_only=recruit_only, event_only=event_only))
    if game == 'genshin':
        for key in data.keys():
            if key.find('旅行者') != -1:
                continue
            tmp_lst.append(Operator(name=key, star=int(data[key]['稀有度'][:1]), limited=False))
    if game == 'pretty':
        for key in data.keys():
            tmp_lst.append(Operator(name=key, star=data[key]['初始星级'], limited=False))
    if game == 'pretty_card':
        for key in data.keys():
            tmp_lst.append(Operator(name=data[key]['中文名'], star=len(data[key]['稀有度']), limited=False))
    return tmp_lst

