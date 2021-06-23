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
            if '干员寻访' not in data[key]['获取途径'] and '公开招募' in data[key]['获取途径']:
                recruit_only = True
            if '活动获取' in data[key]['获取途径']:
                event_only = True
            if '干员寻访' not in data[key]['获取途径'] and '凭证交易所' == data[key]['获取途径'][0]:
                limited = True
            if '干员寻访' not in data[key]['获取途径'] and '信用累计奖励' == data[key]['获取途径'][0]:
                limited = True
            if key.find('阿米娅') != -1:
                continue
            tmp_lst.append(Operator(name=key, star=int(data[key]['星级']),
                                    limited=limited, recruit_only=recruit_only, event_only=event_only))
    if game == 'genshin':
        for key in data.keys():
            if key.find('旅行者') != -1:
                continue
            limited = False
            if data[key]['常驻/限定'] == '限定UP':
                limited = True
            tmp_lst.append(Operator(name=key, star=int(data[key]['稀有度'][:1]), limited=limited))
    if game == 'genshin_arms':
        for key in data.keys():
            if data[key]['获取途径'].find('祈愿') != -1:
                limited = False
                if data[key]['获取途径'].find('限定祈愿') != -1:
                    limited = True
                tmp_lst.append(Operator(name=key, star=int(data[key]['稀有度'][:1]), limited=limited))
    if game == 'pretty':
        for key in data.keys():
            tmp_lst.append(Operator(name=key, star=data[key]['初始星级'], limited=False))
    if game == 'pretty_card':
        for key in data.keys():
            limited = False
            if '卡池' not in data[key]['获取方式']:
                limited = True
            if not data[key]['获取方式']:
                limited = False
            tmp_lst.append(Operator(name=data[key]['中文名'], star=len(data[key]['稀有度']), limited=limited))
    if game in ['guardian', 'guardian_arms']:
        for key in data.keys():
            tmp_lst.append(Operator(name=data[key]['名称'], star=int(data[key]['星级']), limited=False))
    if game == 'pcr':
        for key in data.keys():
            limited = False
            if key.find('（') != -1:
                limited = True
            tmp_lst.append(Operator(name=data[key]['名称'], star=int(data[key]['星级']), limited=limited))
    if game == 'azur':
        for key in data.keys():
            limited = False
            if '可以建造' not in data[key]['获取途径']:
                limited = True
            tmp_lst.append(Operator(name=data[key]['名称'], star=int(data[key]['星级']),
                                    limited=limited, itype=data[key]['类型']))
    if game in ['fgo', 'fgo_card']:
        for key in data.keys():
            limited = False
            try:
                if "圣晶石召唤" not in data[key]['入手方式'] and "圣晶石召唤（Story卡池）" not in data[key]['入手方式']:
                    limited = True
            except KeyError:
                pass
            tmp_lst.append(Operator(name=data[key]['名称'], star=int(data[key]['星级']), limited=limited))
    if game == 'onmyoji':
        for key in data.keys():
            limited = False
            if key in ['奴良陆生', '卖药郎', '鬼灯', '阿香', '蜜桃&芥子', '犬夜叉', '杀生丸', '桔梗', '朽木露琪亚', '黑崎一护',
                       '灶门祢豆子', '灶门炭治郎']:
                limited = True
            tmp_lst.append(Operator(name=data[key]['名称'], star=data[key]['星级'], limited=limited))
    # print(tmp_lst)
    return tmp_lst

