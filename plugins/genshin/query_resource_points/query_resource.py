from urllib import request
from PIL import Image, ImageMath
from io import BytesIO
import json
import os
import time
import base64
from configs.path_config import IMAGE_PATH
from util.init_result import image
import asyncio
import nonebot

driver: nonebot.Driver = nonebot.get_driver()

LABEL_URL = 'https://api-static.mihoyo.com/common/blackboard/ys_obc/v1/map/label/tree?app_sn=ys_obc'
POINT_LIST_URL = 'https://api-static.mihoyo.com/common/blackboard/ys_obc/v1/map/point/list?map_id=2&app_sn=ys_obc'

header = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
         'Chrome/84.0.4147.105 Safari/537.36'

FILE_PATH = os.path.dirname(__file__)

MAP_PATH = None
MAP_IMAGE = None
MAP_SIZE = None

# resource_point里记录的坐标是相对坐标，是以蒙德城的大雕像为中心的，所以图片合成时需要转换坐标
CENTER = (3505, 1907)

zoom = 0.75
resource_icon_offset = (-int(150 * 0.5 * zoom), -int(150 * zoom))


@driver.on_startup
async def init():
    global MAP_SIZE, MAP_PATH, MAP_IMAGE
    MAP_PATH = os.path.join(IMAGE_PATH, "genshin", "seek_god_eye", "icon", "map_icon.jpg")
    MAP_IMAGE = await asyncio.get_event_loop().run_in_executor(None, Image.open, MAP_PATH)
    MAP_SIZE = MAP_IMAGE.size
    await asyncio.get_event_loop().run_in_executor(None, up_label_and_point_list)


data = {
    "all_resource_type": {
        # 这个字典保存所有资源类型，
        # "1": {
        #         "id": 1,
        #         "name": "传送点",
        #         "icon": "",
        #         "parent_id": 0,
        #         "depth": 1,
        #         "node_type": 1,
        #         "jump_type": 0,
        #         "jump_target_id": 0,
        #         "display_priority": 0,
        #         "children": []
        #     },
    },
    "can_query_type_list": {
        # 这个字典保存所有可以查询的资源类型名称和ID，这个字典只有名称和ID
        # 上边字典里"depth": 2的类型才可以查询，"depth": 1的是1级目录，不能查询
        # "七天神像":"2"
        # "风神瞳":"5"

    },
    "all_resource_point_list": [
        # 这个列表保存所有资源点的数据
        # {
        #     "id": 2740,
        #     "label_id": 68,
        #     "x_pos": -1789,
        #     "y_pos": 2628,
        #     "author_name": "✟紫灵心✟",
        #     "ctime": "2020-10-29 10:41:21",
        #     "display_state": 1
        # },
    ],
    "date": ""  # 记录上次更新"all_resource_point_list"的日期
}


def up_icon_image(sublist):
    # 检查是否有图标，没有图标下载保存到本地
    id = sublist["id"]
    icon_url = sublist["icon"]

    icon_path = os.path.join(FILE_PATH, "icon", f"{id}.png")

    if not os.path.exists(icon_path):
        schedule = request.Request(icon_url)
        schedule.add_header('User-Agent', header)
        with request.urlopen(schedule) as f:
            icon = Image.open(f)
            icon = icon.resize((150, 150))

            box_alpha = Image.open(os.path.join(FILE_PATH, "icon", "box_alpha.png")).getchannel("A")
            box = Image.open(os.path.join(FILE_PATH, "icon", "box.png"))

            try:
                icon_alpha = icon.getchannel("A")
                icon_alpha = ImageMath.eval("convert(a*b/256, 'L')", a=icon_alpha, b=box_alpha)
            except ValueError:
                # 米游社的图有时候会没有alpha导致报错，这时候直接使用box_alpha当做alpha就行
                icon_alpha = box_alpha

            icon2 = Image.new("RGBA", (150, 150), "#00000000")
            icon2.paste(icon, (0, -10))

            bg = Image.new("RGBA", (150, 150), "#00000000")
            bg.paste(icon2, mask=icon_alpha)
            bg.paste(box, mask=box)

            with open(icon_path, "wb") as icon_file:
                bg.save(icon_file)


def up_label_and_point_list():
    # 更新label列表和资源点列表

    schedule = request.Request(LABEL_URL)
    schedule.add_header('User-Agent', header)
    with request.urlopen(schedule, timeout=5) as f:
        if f.code != 200:  # 检查返回的状态码是否是200
            raise ValueError(f"资源标签列表初始化失败，错误代码{f.code}")
        label_data = json.loads(f.read().decode('utf-8'))

        for label in label_data["data"]["tree"]:
            data["all_resource_type"][str(label["id"])] = label

            for sublist in label["children"]:
                data["all_resource_type"][str(sublist["id"])] = sublist
                data["can_query_type_list"][sublist["name"]] = str(sublist["id"])
                up_icon_image(sublist)

            label["children"] = []

    schedule = request.Request(POINT_LIST_URL)
    schedule.add_header('User-Agent', header)
    with request.urlopen(schedule) as f:
        if f.code != 200:  # 检查返回的状态码是否是200
            raise ValueError(f"资源点列表初始化失败，错误代码{f.code}")
        test = json.loads(f.read().decode('utf-8'))
        data["all_resource_point_list"] = test["data"]["point_list"]

    data["date"] = time.strftime("%d")


# def load_resource_type_id():
#     with open(os.path.join(FILE_PATH,'resource_type_id.json'), 'r', encoding='UTF-8') as f:
#         json_data = json.load(f)
#         for id in json_data.keys():
#             data["all_resource_type"][id] = json_data[id]
#             if json_data[id]["depth"] != 1:
#                 data["can_query_type_list"][json_data[id]["name"]] = id


# 初始化
# load_resource_type_id()


class Resource_map(object):

    def __init__(self, resource_name):
        self.resource_id = str(data["can_query_type_list"][resource_name])

        # 地图要要裁切的左上角和右下角坐标
        # 这里初始化为地图的大小
        self.x_start = MAP_SIZE[0]
        self.y_start = MAP_SIZE[1]
        self.x_end = 0
        self.y_end = 0

        self.map_image = MAP_IMAGE.copy()

        self.resource_icon = Image.open(self.get_icon_path())
        self.resource_icon = self.resource_icon.resize((int(150 * zoom), int(150 * zoom)))

        self.resource_xy_list = self.get_resource_point_list()

    def get_icon_path(self):
        # 检查有没有图标，有返回正确图标，没有返回默认图标
        icon_path = os.path.join(FILE_PATH, "icon", f"{self.resource_id}.png")

        if os.path.exists(icon_path):
            return icon_path
        else:
            return os.path.join(FILE_PATH, "icon", "0.png")

    def get_resource_point_list(self):
        temp_list = []
        for resource_point in data["all_resource_point_list"]:
            if str(resource_point["label_id"]) == self.resource_id:
                # 获取xy坐标，然后加上中心点的坐标完成坐标转换
                x = resource_point["x_pos"] + CENTER[0]
                y = resource_point["y_pos"] + CENTER[1]
                temp_list.append((int(x), int(y)))
        return temp_list

    def paste(self):
        for x, y in self.resource_xy_list:
            # 把资源图片贴到地图上
            self.map_image.paste(self.resource_icon, (x + resource_icon_offset[0], y + resource_icon_offset[1]),
                                 self.resource_icon)

            # 找出4个方向最远的坐标，用于后边裁切
            self.x_start = min(x, self.x_start)
            self.y_start = min(y, self.y_start)
            self.x_end = max(x, self.x_end)
            self.y_end = max(y, self.y_end)

    def crop(self):

        # 先把4个方向扩展150像素防止把资源图标裁掉
        self.x_start -= 150
        self.y_start -= 150
        self.x_end += 150
        self.y_end += 150

        # 如果图片裁切的太小会看不出资源的位置在哪，检查图片裁切的长和宽看够不够1000，不到1000的按1000裁切
        if (self.x_end - self.x_start) < 1000:
            center = int((self.x_end + self.x_start) / 2)
            self.x_start = center - 500
            self.x_end = center + 500
        if (self.y_end - self.y_start) < 1000:
            center = int((self.y_end + self.y_start) / 2)
            self.y_start = center - 500
            self.y_end = center + 500

        self.map_image = self.map_image.crop((self.x_start, self.y_start, self.x_end, self.y_end))

    def get_cq_cod(self):

        if not self.resource_xy_list:
            return "没有这个资源的信息"

        self.paste()

        self.crop()

        bio = BytesIO()
        self.map_image.save(bio, format='JPEG')
        base64_str = 'base64://' + base64.b64encode(bio.getvalue()).decode()

        return image(b64=base64_str)

    def get_resource_count(self):
        return len(self.resource_xy_list)


def get_resource_map_mes(name):
    if data["date"] != time.strftime("%d"):
        up_label_and_point_list()

    if not (name in data["can_query_type_list"]):
        return f"没有 {name} 这种资源。\n发送 原神资源列表 查看所有资源名称"

    map = Resource_map(name)
    count = map.get_resource_count()

    if not count:
        return f"没有找到 {name} 资源的位置，可能米游社wiki还没更新。"

    mes = f"资源 {name} 的位置如下\n"
    mes += map.get_cq_cod()

    mes += f"\n\n※ {name} 一共找到 {count} 个位置点\n※ 数据来源于米游社wiki"
    return mes


def get_resource_list_mes():
    temp = {}

    for id in data["all_resource_type"].keys():
        # 先找1级目录
        if data["all_resource_type"][id]["depth"] == 1:
            temp[id] = []

    for id in data["all_resource_type"].keys():
        # 再找2级目录
        if data["all_resource_type"][id]["depth"] == 2:
            temp[str(data["all_resource_type"][id]["parent_id"])].append(id)

    mes = "当前资源列表如下：\n"

    for resource_type_id in temp.keys():

        if resource_type_id in ["1", "12", "50", "51", "95", "131"]:
            # 在游戏里能查到的数据这里就不列举了，不然消息太长了
            continue

        mes += f"{data['all_resource_type'][resource_type_id]['name']}："
        for resource_id in temp[resource_type_id]:
            mes += f"{data['all_resource_type'][resource_id]['name']}，"
        mes += "\n"

    return mes
