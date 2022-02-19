from configs.path_config import IMAGE_PATH, TEXT_PATH
from utils.image_utils import BuildImage
from typing import Tuple, List
from math import sqrt, pow
import random

try:
    import ujson as json
except ModuleNotFoundError:
    import json

icon_path = IMAGE_PATH / "genshin" / "genshin_icon"
map_path = IMAGE_PATH / "genshin" / "map" / "map.png"
resource_label_file = TEXT_PATH / "genshin" / "resource_label_file.json"
resource_point_file = TEXT_PATH / "genshin" / "resource_point_file.json"


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
        ratio: float = 1,
    ):
        """
        参数：
            :param resource_name: 资源名称
            :param center_point: 中心点
            :param deviation: 坐标误差
            :param padding: 截图外边距
            :param planning_route: 是否规划最佳线路
            :param ratio: 压缩比率
        """
        self.map = BuildImage(0, 0, background=map_path)
        self.resource_name = resource_name
        self.center_x = center_point[0]
        self.center_y = center_point[1]
        self.deviation = deviation
        self.padding = int(padding * ratio)
        self.planning_route = planning_route
        self.ratio = ratio

        self.deviation = (
            int(self.deviation[0] * ratio),
            int(self.deviation[1] * ratio),
        )

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
            Resources(
                int((self.center_x + data[x]["x_pos"]) * ratio),
                int((self.center_y + data[x]["y_pos"]) * ratio),
            )
            for x in data
            if x != "CENTER_POINT" and data[x]["label_id"] == self.resource_id
        ]
        # 传送锚点坐标
        self.teleport_anchor_point = [
            Resources(
                int((self.center_x + data[x]["x_pos"]) * ratio),
                int((self.center_y + data[x]["y_pos"]) * ratio),
            )
            for x in data
            if x != "CENTER_POINT" and data[x]["label_id"] == self.teleport_anchor_id
        ]
        # 神像坐标
        self.teleport_god_point = [
            Resources(
                int((self.center_x + data[x]["x_pos"]) * ratio),
                int((self.center_y + data[x]["y_pos"]) * ratio),
            )
            for x in data
            if x != "CENTER_POINT" and data[x]["label_id"] == self.teleport_god_id
        ]

    # 将地图上生成资源图标
    def generate_resource_icon_in_map(self) -> int:
        x_list = [x.x for x in self.resource_point]
        y_list = [x.y for x in self.resource_point]
        min_width = min(x_list) - self.padding
        max_width = max(x_list) + self.padding
        min_height = min(y_list) - self.padding
        max_height = max(y_list) + self.padding
        self._generate_transfer_icon((min_width, min_height, max_width, max_height))
        for res in self.resource_point:
            icon = self._get_icon_image(self.resource_id)
            self.map.paste(
                icon, (res.x - self.deviation[0], res.y - self.deviation[1]), True
            )
        if self.planning_route:
            self._generate_best_route()
        self.map.crop((min_width, min_height, max_width, max_height))
        rand = random.randint(1, 10000)
        self.map.save(f"{IMAGE_PATH}/temp/genshin_map_{rand}.png")
        return rand

    # 资源数量
    def get_resource_count(self) -> int:
        return len(self.resource_point)

    # 生成传送锚点和神像
    def _generate_transfer_icon(self, box: Tuple[int, int, int, int]):
        min_width, min_height, max_width, max_height = box
        for resources in [self.teleport_anchor_point, self.teleport_god_point]:
            id_ = (
                self.teleport_anchor_id
                if resources == self.teleport_anchor_point
                else self.teleport_god_id
            )
            for res in resources:
                if min_width < res.x < max_width and min_height < res.y < max_height:
                    icon = self._get_icon_image(id_)
                    self.map.paste(
                        icon,
                        (res.x - self.deviation[0], res.y - self.deviation[1]),
                        True,
                    )

    # 生成最优路线（说是最优其实就是直线最短）
    def _generate_best_route(self):
        line_points = []
        teleport_list = self.teleport_anchor_point + self.teleport_god_point
        for teleport in teleport_list:
            current_res, res_min_distance = teleport.get_resource_distance(self.resource_point)
            current_teleport, teleport_min_distance = current_res.get_resource_distance(teleport_list)
            if current_teleport == teleport:
                self.map.line(
                    (current_teleport.x, current_teleport.y, current_res.x, current_res.y), (255, 0, 0), width=1
                )
        is_used_res_points = []
        for res in self.resource_point:
            if res in is_used_res_points:
                continue
            current_teleport, teleport_min_distance = res.get_resource_distance(teleport_list)
            current_res, res_min_distance = res.get_resource_distance(self.resource_point)
            if teleport_min_distance < res_min_distance:
                self.map.line(
                    (current_teleport.x, current_teleport.y, res.x, res.y), (255, 0, 0), width=1
                )
            else:
                is_used_res_points.append(current_res)
                self.map.line(
                    (current_res.x, current_res.y, res.x, res.y), (255, 0, 0), width=1
                )
                res_cp = self.resource_point[:]
                res_cp.remove(current_res)
                # for _ in res_cp:
                current_teleport_, teleport_min_distance = res.get_resource_distance(teleport_list)
                current_res, res_min_distance = res.get_resource_distance(res_cp)
                if teleport_min_distance < res_min_distance:
                    self.map.line(
                        (current_teleport.x, current_teleport.y, res.x, res.y), (255, 0, 0), width=1
                    )
                else:
                    self.map.line(
                        (current_res.x, current_res.y, res.x, res.y), (255, 0, 0), width=1
                    )
                    is_used_res_points.append(current_res)
            is_used_res_points.append(res)

        # resources_route = []
        # # 先连上最近的资源路径
        # for res in self.resource_point:
        #     # 拿到最近的资源
        #     current_res, _ = res.get_resource_distance(
        #         self.resource_point
        #         + self.teleport_anchor_point
        #         + self.teleport_god_point
        #     )
        #     self.map.line(
        #         (current_res.x, current_res.y, res.x, res.y), (255, 0, 0), width=1
        #     )
            # resources_route.append((current_res, res))
        # teleport_list = self.teleport_anchor_point + self.teleport_god_point
        # for res1, res2 in resources_route:
        #     point_list = [x for x in resources_route if res1 in x or res2 in x]
        #     if not list(set(point_list).intersection(set(teleport_list))):
        #         if res1 not in teleport_list and res2 not in teleport_list:
        #             # while True:
        #             #     tmp = [x for x in point_list]
        #             #     break
        #             teleport1, distance1 = res1.get_resource_distance(teleport_list)
        #             teleport2, distance2 = res2.get_resource_distance(teleport_list)
        #             if distance1 > distance2:
        #                 self.map.line(
        #                     (teleport1.x, teleport1.y, res1.x, res1.y),
        #                     (255, 0, 0),
        #                     width=1,
        #                 )
        #             else:
        #                 self.map.line(
        #                     (teleport2.x, teleport2.y, res2.x, res2.y),
        #                     (255, 0, 0),
        #                     width=1,
        #                 )

        # self.map.line(xy, (255, 0, 0), width=3)

    # 获取资源图标
    def _get_icon_image(self, id_: int) -> "BuildImage":
        icon = icon_path / f"{id_}.png"
        if icon.exists():
            return BuildImage(
                int(50 * self.ratio), int(50 * self.ratio), background=icon
            )
        return BuildImage(
            int(50 * self.ratio),
            int(50 * self.ratio),
            background=f"{icon_path}/box.png",
        )

    # def _get_shortest_path(self, res: 'Resources', res_2: 'Resources'):


# 资源类
class Resources:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_distance(self, x: int, y: int):
        return int(sqrt(pow(abs(self.x - x), 2) + pow(abs(self.y - y), 2)))

    # 拿到资源在该列表中的最短路径
    def get_resource_distance(self, resources: List["Resources"]) -> "Resources, int":
        current_res = None
        min_distance = 999999
        for res in resources:
            distance = self.get_distance(res.x, res.y)
            if distance < min_distance and res != self:
                current_res = res
                min_distance = distance
        return current_res, min_distance





