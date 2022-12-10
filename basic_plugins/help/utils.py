from typing import List, Tuple, Dict, Optional
from configs.path_config import IMAGE_PATH
from utils.image_utils import BuildImage
from configs.config import Config
import os
import random

from utils.manager import plugin_data_manager, group_manager
from utils.manager.models import PluginData, PluginType

background_path = IMAGE_PATH / "background" / "help" / "simple_help"


async def build_help_image(image_group: List[List[BuildImage]], h: int):
    bk = None
    random_bk = os.listdir(background_path)
    if random_bk:
        bk = random.choice(random_bk)
    A = BuildImage(
        h,
        h,
        font_size=24,
        color="#FFEFD5",
        background=(background_path / bk) if bk else None,
    )
    A.filter("GaussianBlur", 5)
    curr_w = 50
    for ig in image_group:
        curr_h = 180
        for img in ig:
            await A.apaste(img, (curr_w, curr_h), True)
            curr_h += img.h + 10
        curr_w += max([x.w for x in ig]) + 30
    return A


def group_image(image_list: List[BuildImage]) -> Tuple[List[List[BuildImage]], int]:
    """
    说明:
        根据图片大小进行分组
    参数:
        :param image_list: 排序图片列表
    """
    image_list.sort(key=lambda x: x.h, reverse=True)
    max_image = max(image_list, key=lambda x: x.h)

    image_list.remove(max_image)
    max_h = max_image.h
    total_w = 0

    # 图片分组
    image_group = [[max_image]]
    is_use = []
    surplus_list = image_list[:]

    for image in image_list:
        if image.uid not in is_use:
            group = [image]
            is_use.append(image.uid)
            curr_h = image.h
            while True:
                surplus_list = [x for x in surplus_list if x.uid not in is_use]
                for tmp in surplus_list:
                    temp_h = curr_h + tmp.h + 10
                    if temp_h < max_h or abs(max_h - temp_h) < 100:
                        curr_h += tmp.h + 15
                        is_use.append(tmp.uid)
                        group.append(tmp)
                        break
                else:
                    break
            total_w += max([x.w for x in group]) + 15
            image_group.append(group)
    while surplus_list:
        surplus_list = [x for x in surplus_list if x.uid not in is_use]
        if not surplus_list:
            break
        surplus_list.sort(key=lambda x: x.h, reverse=True)
        for img in surplus_list:
            if img.uid not in is_use:
                _w = 0
                index = -1
                for i, ig in enumerate(image_group):
                    if s := sum([x.h for x in ig]) > _w:
                        _w = s
                        index = i
                if index != -1:
                    image_group[index].append(img)
                    is_use.append(img.uid)
    max_h = 0
    max_w = 0
    for i, ig in enumerate(image_group):
        if (_h := sum([x.h + 15 for x in ig])) > max_h:
            max_h = _h
        max_w += max([x.w for x in ig]) + 30
    is_use.clear()
    while abs(max_h - max_w) > 200 and len(image_group) - 1 >= len(image_group[-1]):
        for img in image_group[-1]:
            _min_h = 0
            _min_index = -1
            for i, ig in enumerate(image_group):
                if i not in is_use and (_h := sum([x.h for x in ig]) + img.h) > _min_h:
                    _min_h = _h
                    _min_index = i
            is_use.append(_min_index)
            image_group[_min_index].append(img)
        max_w -= max([x.w for x in image_group[-1]])
        image_group.pop(-1)
    return image_group, max(max_h + 250, max_w + 70)


class HelpImageBuild:

    build: Optional["HelpImageBuild"] = None

    def __init__(self):
        self._data: Dict[str, PluginData] = plugin_data_manager.get_data()
        self._sort_data: Dict[str, List[PluginData]] = {}
        self._image_list = []

    def __new__(cls, *args, **kwargs):
        if not cls.build:
            cls.build = super().__new__(cls)
        return cls.build

    def sort_type(self):
        """
        说明:
            对插件按照菜单类型分类
        """
        for key in self._data.keys():
            plugin_data = self._data[key]
            if plugin_data.plugin_type == PluginType.NORMAL:
                if not self._sort_data.get(plugin_data.menu_type[0]):
                    self._sort_data[plugin_data.menu_type[0]] = []
                self._sort_data[plugin_data.menu_type[0]].append(self._data[key])

    async def build_name_image(
        self,
        max_width: int,
        name: str,
        color: str,
        text_color: Tuple[int, int, int],
        pos: Optional[Tuple[int, int, int, int]],
    ) -> BuildImage:
        image = BuildImage(max_width - 5, 50, color=color, font_size=24)
        await image.acircle_corner()
        await image.atext((0, 0), name, text_color, center_type="center")
        return image

    async def build_image(self, group_id: Optional[int]) -> BuildImage:
        """
        说明:
            构造帮助图片
        参数:
            :param group_id: 群号
        """
        self._image_list = []
        self.sort_type()
        font_size = 24
        build_type = Config.get_config("help", "TYPE")
        _image = BuildImage(0, 0, plain_text="1", font_size=font_size)
        for idx, menu_type in enumerate(self._sort_data.keys()):
            plugin_list = self._sort_data[menu_type]
            wh_list = [_image.getsize(x.name) for x in plugin_list]
            wh_list.append(_image.getsize(menu_type))
            # sum_height = sum([x[1] for x in wh_list])
            if build_type == "VV":
                sum_height = 50 * len(plugin_list) + 10
            else:
                sum_height = (font_size + 6) * len(plugin_list) + 10
            max_width = max([x[0] for x in wh_list]) + 20
            bk = BuildImage(
                max_width + 40,
                sum_height + 50,
                font_size=30,
                color="#a7d1fc",
                font="CJGaoDeGuo.otf",
            )
            title_size = bk.getsize(menu_type)
            max_width = max_width if max_width > title_size[0] else title_size[0]
            B = BuildImage(
                max_width + 40,
                sum_height,
                font_size=font_size,
                color="white" if not idx % 2 else "black",
            )
            curr_h = 10
            for i, plugin_data in enumerate(plugin_list):
                text_color = (255, 255, 255) if idx % 2 else (0, 0, 0)
                if group_id and not group_manager.get_plugin_status(
                    plugin_data.model, group_id
                ):
                    text_color = (252, 75, 13)
                pos = None
                # 禁用状态划线
                if (
                    not plugin_data.plugin_status.status
                    and plugin_data.plugin_status.block_type in ["group", "all"]
                ) or not group_manager.get_plugin_super_status(plugin_data.model, group_id):
                    w = curr_h + int(B.getsize(plugin_data.name)[1] / 2) + 2
                    pos = (
                        7,
                        w,
                        B.getsize(plugin_data.name)[0] + 35,
                        w,
                    )
                if build_type == "VV":
                    name_image = await self.build_name_image(
                        max_width,
                        plugin_data.name,
                        "black" if not idx % 2 else "white",
                        text_color,
                        pos,
                    )
                    await B.apaste(
                        name_image, (0, curr_h), True, center_type="by_width"
                    )
                    curr_h += name_image.h + 5
                else:
                    await B.atext(
                        (10, curr_h), f"{i + 1}.{plugin_data.name}", text_color
                    )
                    if pos:
                        await B.aline(pos, (236, 66, 7), 3)
                    curr_h += font_size + 5
            if menu_type == "normal":
                menu_type = "功能"
            await bk.atext((0, 14), menu_type, center_type="by_width")
            await bk.apaste(B, (0, 50))
            await bk.atransparent(2)
            # await bk.acircle_corner(point_list=['lt', 'rt'])
            self._image_list.append(bk)
        image_group, h = group_image(self._image_list)
        B = await build_help_image(image_group, h)
        w = 10
        h = 10
        for msg in [
            "目前支持的功能列表:",
            "可以通过 ‘帮助[功能名称]’ 来获取对应功能的使用方法",
            "或者使用 ‘详细帮助’ 来获取所有功能方法",
        ]:
            text = BuildImage(
                0,
                0,
                plain_text=msg,
                font_size=24,
                font="HYWenHei-85W.ttf",
            )
            B.paste(text, (w, h), True)
            h += 50
            if msg == "目前支持的功能列表:":
                w += 50
        await B.apaste(
            BuildImage(
                0,
                0,
                plain_text="注: 红字代表功能被群管理员禁用，红线代表功能正在维护",
                font_size=24,
                font="HYWenHei-85W.ttf",
                font_color=(231, 74, 57),
            ),
            (300, 10),
            True,
        )
        return B
