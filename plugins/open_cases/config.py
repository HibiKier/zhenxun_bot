import random
import pypinyin

BLUE = 0.7981
BLUE_ST = 0.0699
PURPLE = 0.1626
PURPLE_ST = 0.0164
PINK = 0.0315
PINK_ST = 0.0048
RED = 0.0057
RED_ST = 0.00021
KNIFE = 0.0021
KNIFE_ST = 0.000041

# 崭新
FACTORY_NEW_S = 0
FACTORY_NEW_E = 0.0699999
# 略磨
MINIMAL_WEAR_S = 0.07
MINIMAL_WEAR_E = 0.14999
# 久经
FIELD_TESTED_S = 0.15
FIELD_TESTED_E = 0.37999
# 破损
WELL_WORN_S = 0.38
WELL_WORN_E = 0.44999
# 战痕
BATTLE_SCARED_S = 0.45
BATTLE_SCARED_E = 0.99999

# 狂牙大行动
KUANGYADAXINGDONG_CASE_KNIFE = ['摩托手套 | 第三特种兵连', '狂牙手套 | 翡翠', '驾驶手套 | 美洲豹女王', '运动手套 | 弹弓', '专业手套 | 老虎精英'
                                , '专业手套 | 渐变大理石', '运动手套 | 夜行衣', '驾驶手套 | 西装革履', '摩托手套 | 终点线', '摩托手套 | 血压',
                                '运动手套 | 猩红头巾', '驾驶手套 | 雪豹', '裹手 | 长颈鹿', '驾驶手套 | 绯红列赞', '裹手 | 沙漠头巾',
                                '专业手套 | 一线特工', '狂牙手套 | 黄色斑纹', '摩托手套 | 小心烟幕弹', '裹手 | 蟒蛇', '裹手 | 警告！',
                                '狂牙手套 | 精神错乱', '运动手套 | 大型猎物', '狂牙手套 | 针尖', '专业手套 | 陆军少尉长官']
KUANGYADAXINGDONG_CASE_RED = ['M4A1 | 印花集', '格洛克 | 黑色魅影']
KUANGYADAXINGDONG_CASE_PINK = ['FN57 | 童话城堡', 'M4A4 | 赛博', 'USP | 小绿怪']
KUANGYADAXINGDONG_CASE_PURPLE = ['AWP | 亡灵之主', '双持贝瑞塔 | 灾难', '新星 | 一见青心', 'SSG 08 | 抖枪', 'UMP-45 | 金铋辉煌']
KUANGYADAXINGDONG_CASE_BLUE = ['CZ75 | 世仇', 'P90 | 大怪兽RUSH', 'G3SG1 | 血腥迷彩', '加利尔 AR | 破坏者', 'P250 | 污染物',
                               'M249 | 等高线', 'MP5-SD | 零点行动']

# 突围大行动
TUWEIDAXINGDONG_CASE_KNIFE = ['蝴蝶刀 | 无涂装', '蝴蝶刀 | 蓝钢', '蝴蝶刀 | 屠夫', '蝴蝶刀 | 森林 DDPAT', '蝴蝶刀 | 北方森林',
                              '蝴蝶刀 | 狩猎网格', '蝴蝶刀 | 枯焦之色', '蝴蝶刀 | 人工染色', '蝴蝶刀 | 都市伪装', '蝴蝶刀 | 表面淬火',
                              '蝴蝶刀 | 深红之网', '蝴蝶刀 | 渐变之色', '蝴蝶刀 | 噩梦之夜']
TUWEIDAXINGDONG_CASE_RED = ['P90 | 二西莫夫', 'M4A1 | 次时代']
TUWEIDAXINGDONG_CASE_PINK = ['沙漠之鹰 | 阴谋者', 'FN57 | 狩猎利器', '格洛克 | 水灵']
TUWEIDAXINGDONG_CASE_PURPLE = ['PP-野牛 | 死亡主宰者', 'CZ75 | 猛虎', '新星 | 锦鲤', 'P250 | 超新星']
TUWEIDAXINGDONG_CASE_BLUE = ['MP7 | 都市危机', '内格夫 | 沙漠精英', 'P2000 | 乳白象牙', 'SSG 08 | 无尽深海', 'UMP-45 | 迷之宫']


# 命悬一线
MINGXUANYIXIAN_CASE_KNIFE = ['专业手套 | 大腕', '专业手套 | 深红之网', '专业手套 | 渐变之色', '专业手套 | 狩鹿', '九头蛇手套 | 响尾蛇',
                             '九头蛇手套 | 红树林', '九头蛇手套 | 翡翠色调', '九头蛇手套 | 表面淬火', '摩托手套 | 交运', '摩托手套 | 嘭！',
                             '摩托手套 | 多边形', '摩托手套 | 玳瑁', '裹手 | 套印', '裹手 | 森林色调', '裹手 | 钴蓝骷髅', '裹手 | 防水布胶带',
                             '运动手套 | 双栖', '运动手套 | 欧米伽', '运动手套 | 迈阿密风云', '运动手套 | 青铜形态', '驾驶手套 | 墨绿色调',
                             '驾驶手套 | 王蛇', '驾驶手套 | 蓝紫格子', '驾驶手套 | 超越']
MINGXUANYIXIAN_CASE_RED = ['M4A4 | 黑色魅影', 'MP7 | 血腥运动']
MINGXUANYIXIAN_CASE_PINK = ['AUG | 湖怪鸟', 'AWP | 死神', 'USP | 脑洞大开']
MINGXUANYIXIAN_CASE_PURPLE = ['MAG-7 | SWAG-7', 'UMP-45 | 白狼', '内格夫 | 狮子鱼', '新星 | 狂野六号', '格洛克 | 城里的月光']
MINGXUANYIXIAN_CASE_BLUE = ['FN57 | 焰色反应', 'MP9 | 黑砂', 'P2000 | 都市危机', 'PP-野牛 | 黑夜暴乱', 'R8 左轮手枪 | 稳',
                            'SG 553 | 阿罗哈', 'XM1014 | 锈蚀烈焰']


LIEKONG_CASE_KNIFE = ['求生匕首 | 无涂装', '求生匕首 | 人工染色', '求生匕首 | 北方森林', '求生匕首 | 夜色', '求生匕首 | 屠夫',
                      '求生匕首 | 枯焦之色', '求生匕首 | 森林 DDPAT', '求生匕首 | 深红之网', '求生匕首 | 渐变之色', '求生匕首 | 狩猎网格',
                      '求生匕首 | 蓝钢', '求生匕首 | 表面淬火', '求生匕首 | 都市伪装', '流浪者匕首 | 无涂装', '流浪者匕首 | 人工染色',
                      '流浪者匕首 | 北方森林', '流浪者匕首 | 夜色', '流浪者匕首 | 屠夫', '流浪者匕首 | 枯焦之色', '流浪者匕首 | 森林 DDPAT',
                      '流浪者匕首 | 深红之网', '流浪者匕首 | 渐变之色', '流浪者匕首 | 狩猎网格', '流浪者匕首 | 蓝钢', '流浪者匕首 | 表面淬火',
                      '流浪者匕首 | 都市伪装', '系绳匕首 | 无涂装', '系绳匕首 | 人工染色', '系绳匕首 | 北方森林', '系绳匕首 | 夜色',
                      '系绳匕首 | 屠夫', '系绳匕首 | 枯焦之色', '系绳匕首 | 森林 DDPAT', '系绳匕首 | 深红之网', '系绳匕首 | 渐变之色',
                      '系绳匕首 | 狩猎网格', '系绳匕首 | 蓝钢', '系绳匕首 | 表面淬火', '系绳匕首 | 都市伪装', '骷髅匕首 | 无涂装',
                      '骷髅匕首 | 人工染色', '骷髅匕首 | 北方森林', '骷髅匕首 | 夜色', '骷髅匕首 | 屠夫', '骷髅匕首 | 枯焦之色',
                      '骷髅匕首 | 森林 DDPAT', '骷髅匕首 | 深红之网', '骷髅匕首 | 渐变之色', '骷髅匕首 | 狩猎网格', '骷髅匕首 | 蓝钢',
                      '骷髅匕首 | 表面淬火', '骷髅匕首 | 都市伪装']
LIEKONG_CASE_RED = ['AK-47 | 阿努比斯军团', '沙漠之鹰 | 印花集']
LIEKONG_CASE_PINK = ['M4A4 | 齿仙', 'XM1014 | 埋葬之影', '格洛克 | 摩登时代']
LIEKONG_CASE_PURPLE = ['加利尔 AR | 凤凰商号', 'Tec-9 | 兄弟连', 'MP5-SD | 猛烈冲锋', 'MAG-7 | 北冥有鱼', 'MAC-10 | 魅惑']
LIEKONG_CASE_BLUE = ['内格夫 | 飞羽', 'SSG 08 | 主机001', 'SG 553 | 锈蚀之刃', 'PP-野牛 | 神秘碑文', 'P90 | 集装箱', 'P250 | 卡带',
                     'P2000 | 盘根错节']


GUANGPU_CASE_KNIFE = ['弯刀 | 外表生锈', '弯刀 | 多普勒', '弯刀 | 大马士革钢', '弯刀 | 渐变大理石', '弯刀 | 致命紫罗兰', '弯刀 | 虎牙',
                      '暗影双匕 | 外表生锈', '暗影双匕 | 多普勒', '暗影双匕 | 大马士革钢', '暗影双匕 | 渐变大理石', '暗影双匕 | 致命紫罗兰',
                      '暗影双匕 | 虎牙', '猎杀者匕首 | 外表生锈', '猎杀者匕首 | 多普勒', '猎杀者匕首 | 大马士革钢', '猎杀者匕首 | 渐变大理石',
                      '猎杀者匕首 | 致命紫罗兰', '猎杀者匕首 | 虎牙', '蝴蝶刀 | 外表生锈', '蝴蝶刀 | 多普勒', '蝴蝶刀 | 大马士革钢',
                      '蝴蝶刀 | 渐变大理石', '蝴蝶刀 | 致命紫罗兰', '蝴蝶刀 | 虎牙', '鲍伊猎刀 | 外表生锈', '鲍伊猎刀 | 多普勒',
                      '鲍伊猎刀 | 大马士革钢', '鲍伊猎刀 | 渐变大理石', '鲍伊猎刀 | 致命紫罗兰', '鲍伊猎刀 | 虎牙']
GUANGPU_CASE_RED = ['USP | 黑色魅影', 'AK-47 | 血腥运动']
GUANGPU_CASE_PINK = ['M4A1 | 毁灭者 2000', 'CZ75 | 相柳', 'AWP | 浮生如梦']
GUANGPU_CASE_PURPLE = ['加利尔 AR | 深红海啸', 'XM1014 | 四季', 'UMP-45 | 支架', 'MAC-10 | 绝界之行', 'M249 | 翠绿箭毒蛙']
GUANGPU_CASE_BLUE = ['沙漠之鹰 | 锈蚀烈焰', '截短霰弹枪 | 梭鲈', 'SCAR-20 | 蓝图', 'PP-野牛 | 丛林滑流', 'P250 | 涟漪', 'MP7 | 非洲部落',
                     'FN57 | 毛细血管']


NO_STA_KNIFE = ['求生匕首 | 北方森林', '求生匕首 | 夜色', '求生匕首 | 枯焦之色', '流浪者匕首 | 夜色', '流浪者匕首 | 枯焦之色', '流浪者匕首 | 森林 DDPAT',
                '系绳匕首 | 夜色', '系绳匕首 | 狩猎网格', '骷髅匕首 | 夜色', '骷髅匕首 | 森林 DDPAT', '骷髅匕首 | 狩猎网格']


def get_wear(num: float) -> str:
    if num <= FACTORY_NEW_E:
        return "崭新出厂"
    if MINIMAL_WEAR_S <= num <= MINIMAL_WEAR_E:
        return "略有磨损"
    if FIELD_TESTED_S <= num <= FIELD_TESTED_E:
        return "久经沙场"
    if WELL_WORN_S <= num <= WELL_WORN_E:
        return "破损不堪"
    return "战痕累累"


def get_color_quality(rand: float, case_name: str):
    case = ""
    mosun = random.random()/2 + random.random()/2
    for i in pypinyin.pinyin(case_name, style=pypinyin.NORMAL):
        case += ''.join(i)
    case = case.upper()
    CASE_KNIFE = eval(case + "_CASE_KNIFE")
    CASE_RED = eval(case + "_CASE_RED")
    CASE_PINK = eval(case + "_CASE_PINK")
    CASE_PURPLE = eval(case + "_CASE_PURPLE")
    CASE_BLUE = eval(case + "_CASE_BLUE")
    if rand <= KNIFE:
        skin = "罕见级(金色): " + random.choice(CASE_KNIFE)
        if random.random() <= KNIFE_ST and (skin[2:4] != "手套" or skin[:2] != "裹手") and skin.split(':')[1] \
                not in NO_STA_KNIFE:
            skin_sp = skin.split("|")
            skin = skin_sp[0] + "（StatTrak™） | " + skin_sp[1]
    elif KNIFE < rand <= RED:
        skin = "隐秘级(红色): " + random.choice(CASE_RED)
        if random.random() <= RED_ST:
            skin_sp = skin.split("|")
            skin = skin_sp[0] + "（StatTrak™） | " + skin_sp[1]
    elif RED < rand <= PINK:
        skin = "保密级(粉色): " + random.choice(CASE_PINK)
        if random.random() <= PINK_ST:
            skin_sp = skin.split("|")
            skin = skin_sp[0] + "（StatTrak™） | " + skin_sp[1]
    elif PINK < rand <= PURPLE:
        skin = "受限级(紫色): " + random.choice(CASE_PURPLE)
        if random.random() <= PURPLE_ST:
            skin_sp = skin.split("|")
            skin = skin_sp[0] + "（StatTrak™） | " + skin_sp[1]
    else:
        skin = "军规级(蓝色): " + random.choice(CASE_BLUE)
        if random.random() <= BLUE_ST:
            skin_sp = skin.split("|")
            skin = skin_sp[0] + "（StatTrak™） | " + skin_sp[1]
    if skin.find("（") != -1:
        cpskin = skin.split(":")[1]
        ybskin = cpskin.split("|")
        temp_skin = ybskin[0].strip()[:-11] + " | " + ybskin[1].strip()
    else:
        temp_skin = skin.split(":")[1].strip()
    # 崭新 -> 略磨
    if temp_skin in [] or temp_skin.find('渐变之色') != -1 or temp_skin.find('多普勒') != -1 or temp_skin.find('虎牙') != -1\
            or temp_skin.find('渐变大理石') != -1:
        mosun = random.uniform(FACTORY_NEW_S, MINIMAL_WEAR_E) / 2 + random.uniform(FACTORY_NEW_S, MINIMAL_WEAR_E) / 2
    # 崭新 -> 久经
    if temp_skin in ['沙漠之鹰 | 阴谋者', '新星 | 锦鲤'] or temp_skin.find('屠夫') != -1:
        mosun = random.uniform(FACTORY_NEW_S, FIELD_TESTED_E) / 2 + random.uniform(FACTORY_NEW_S, FIELD_TESTED_E) / 2
    # 崭新 -> 破损
    if temp_skin in ['UMP-45 | 迷之宫', 'P250 | 超新星', '系绳匕首 | 深红之网', 'M249 | 翠绿箭毒蛙', 'AK-47 | 血腥运动']:
        mosun = random.uniform(FACTORY_NEW_S, WELL_WORN_E) / 2 + random.uniform(FACTORY_NEW_S, WELL_WORN_E) / 2
    # 破损 -> 战痕
    if temp_skin in [] or temp_skin.find('外表生锈') != -1:
        mosun = random.uniform(WELL_WORN_S, BATTLE_SCARED_E) / 2 + random.uniform(WELL_WORN_S, BATTLE_SCARED_E) / 2
    if mosun > MINIMAL_WEAR_E:
        for _ in range(2):
            if random.random() < 5:
                if random.random() < 0.2:
                    mosun /= 3
                else:
                    mosun /= 2
                break
    skin += " (" + get_wear(mosun) + ")"
    return skin, mosun

# M249（StatTrak™） | 等高线