from pathlib import Path
from configs.path_config import IMAGE_PATH, TXT_PATH
from utils.image_utils import CreateImg
from typing import Tuple
from math import sqrt, pow
import random

try:
    import ujson as json
except ModuleNotFoundError:
    import json

icon_path = Path(IMAGE_PATH) / "genshin" / "genshin_icon"
map_path = Path(IMAGE_PATH) / "genshin" / "map" / "map.png"
resource_label_file = Path(TXT_PATH) / "genshin" / "resource_label_file.json"
resource_point_file = Path(TXT_PATH) / "genshin" / "resource_point_file.json"


class Map:
    """
    原神资源生成类
    """

    def __init__(
        self,
        resource_name: str,
        center_point: Tuple[int, int],
        deviation: Tuple[int, int] = (25, 51),
        padding: int = 100,
        planning_route: bool = False,
    ):
        """
        参数：
            :param resource_name: 资源名称
            :param center_point: 中心点
            :param deviation: 坐标误差
            :param padding: 截图外边距
            :param planning_route: 是否规划最佳线路
        """
        self.map = CreateImg(0, 0, background=map_path)
        self.resource_name = resource_name
        self.center_x = center_point[0]
        self.center_y = center_point[1]
        self.deviation = deviation
        self.padding = padding
        self.planning_route = planning_route

        data = json.load(open(resource_label_file, "r", encoding="utf8"))
        # 资源 id
        self.resource_id = [
            data[x]["id"]
            for x in data
            if x != "CENTER_POINT" and data[x]["name"] == resource_name
        ][0]
        # 传送锚点 id
        self.teleport_anchor_id = [
            data[x]["id"]
            for x in data
            if x != "CENTER_POINT" and data[x]["name"] == "传送锚点"
        ][0]
        # 神像 id
        self.teleport_god_id = [
            data[x]["id"]
            for x in data
            if x != "CENTER_POINT" and data[x]["name"] == "七天神像"
        ][0]
        # 资源坐标
        data = json.load(open(resource_point_file, "r", encoding="utf8"))
        self.resource_point = [
            (
                self.center_x + int(data[x]["x_pos"]),
                self.center_y + int(data[x]["y_pos"]),
            )
            for x in data
            if x != "CENTER_POINT" and data[x]["label_id"] == self.resource_id
        ]
        # 传送锚点坐标
        self.teleport_anchor_point = [
            (
                self.center_x + int(data[x]["x_pos"]),
                self.center_y + int(data[x]["y_pos"]),
            )
            for x in data
            if x != "CENTER_POINT" and data[x]["label_id"] == self.teleport_anchor_id
        ]
        # 神像坐标
        self.teleport_god_point = [
            (
                self.center_x + int(data[x]["x_pos"]),
                self.center_y + int(data[x]["y_pos"]),
            )
            for x in data
            if x != "CENTER_POINT" and data[x]["label_id"] == self.teleport_god_id
        ]

    # 将地图上生成资源图标
    def generate_resource_icon_in_map(self) -> int:
        x_list = [x[0] for x in self.resource_point]
        y_list = [x[1] for x in self.resource_point]
        min_width = min(x_list) - self.padding
        max_width = max(x_list) + self.padding
        min_height = min(y_list) - self.padding
        max_height = max(y_list) + self.padding
        if self.planning_route:
            self._generate_best_route()
        self._generate_transfer_icon((min_width, min_height, max_width, max_height))
        for x, y in self.resource_point:
            icon = self._get_icon_image(self.resource_id)
            self.map.paste(icon, (x - self.deviation[0], y - self.deviation[1]), True)
        self.map.crop((min_width, min_height, max_width, max_height))
        rand = random.randint(1, 10000)
        self.map.save(f'{IMAGE_PATH}/temp/genshin_map_{rand}.png')
        return rand

    # 资源数量
    def get_resource_count(self) -> int:
        return len(self.resource_point)

    # 生成传送锚点和神像
    def _generate_transfer_icon(self, box: Tuple[int, int, int, int]):
        min_width, min_height, max_width, max_height = box
        for points in [self.teleport_anchor_point, self.teleport_god_point]:
            id_ = (
                self.teleport_anchor_id
                if points == self.teleport_anchor_point
                else self.teleport_god_id
            )
            for x, y in points:
                if min_width < x < max_width and min_height < y < max_height:
                    icon = self._get_icon_image(id_)
                    self.map.paste(
                        icon, (x - self.deviation[0], y - self.deviation[1]), True
                    )

    # 生成最优路线（说是最优其实就是直线最短）
    def _generate_best_route(self):
        for x, y in self.resource_point:
            min_deviation = 999999
            xy = None
            for points in [
                self.resource_point,
                self.teleport_anchor_point,
                self.teleport_god_point,
            ]:
                for r_x, r_y in points:
                    distance = int(sqrt(pow(abs(r_x - x), 2) + pow(abs(r_y - y), 2)))
                    if distance < min_deviation and x != r_x and y != r_y:
                        min_deviation = distance
                        xy = (x, y, r_x, r_y)

            self.map.line(xy, (255, 0, 0), width=3)

    # 获取资源图标
    def _get_icon_image(self, id_: int) -> "CreateImg":
        icon = icon_path / f"{id_}.png"
        if icon.exists():
            return CreateImg(50, 50, background=icon)
        return CreateImg(50, 50, background=f"{icon_path}/box.png")
