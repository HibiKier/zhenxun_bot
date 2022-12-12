from typing import List, Tuple, Dict, Optional
from nonebot_plugin_htmlrender import template_to_pic

from ._config import Item
from configs.path_config import IMAGE_PATH, TEMPLATE_PATH, DATA_PATH
from utils.decorator import Singleton
from utils.image_utils import BuildImage
from configs.config import Config
import os
import random

from utils.manager import plugin_data_manager, group_manager
from utils.manager.models import PluginData, PluginType


GROUP_HELP_PATH = DATA_PATH / "group_help"
GROUP_HELP_PATH.mkdir(exist_ok=True, parents=True)
for x in os.listdir(GROUP_HELP_PATH):
    group_help_image = GROUP_HELP_PATH / x
    group_help_image.unlink()

BACKGROUND_PATH = IMAGE_PATH / "background" / "help" / "simple_help"

LOGO_PATH = TEMPLATE_PATH / 'menu' / 'res' / 'logo'


async def build_help_image(image_group: List[List[BuildImage]], h: int):
    bk = None
    random_bk = os.listdir(BACKGROUND_PATH)
    if random_bk:
        bk = random.choice(random_bk)
    A = BuildImage(
        h,
        h,
        font_size=24,
        color="#FFEFD5",
        background=(BACKGROUND_PATH / bk) if bk else None,
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


@Singleton
class HelpImageBuild:

    def __init__(self):
        self._data: Dict[str, PluginData] = plugin_data_manager.get_data()
        self._sort_data: Dict[str, List[PluginData]] = {}
        self._image_list = []
        self.icon2str = {
            'normal': 'fa fa-cog',
            '原神相关': 'fa fa-circle-o',
            '常规插件': 'fa fa-cubes',
            '联系管理员': 'fa fa-envelope-o',
            '抽卡相关': 'fa fa-credit-card-alt',
            '来点好康的': 'fa fa-picture-o',
            '数据统计': 'fa fa-bar-chart',
            '一些工具': 'fa fa-shopping-cart',
            '商店': 'fa fa-shopping-cart',
            '其它': 'fa fa-tags',
            '群内小游戏': 'fa fa-gamepad',
        }

    def sort_type(self):
        """
        说明:
            对插件按照菜单类型分类
        """
        if not self._sort_data.keys():
            for key in self._data.keys():
                plugin_data = self._data[key]
                if plugin_data.plugin_type == PluginType.NORMAL:
                    if not self._sort_data.get(plugin_data.menu_type[0]):
                        self._sort_data[plugin_data.menu_type[0]] = []
                    self._sort_data[plugin_data.menu_type[0]].append(self._data[key])

    async def build_image(self, group_id: Optional[int]):
        if group_id:
            help_image = GROUP_HELP_PATH / f"{group_id}.png"
        else:
            help_image = IMAGE_PATH / f"simple_help.png"
        build_type = Config.get_config("help", "TYPE")
        if build_type == 'HTML':
            byt = await self.build_html_image(group_id)
            with open(help_image, 'wb') as f:
                f.write(byt)
        else:
            img = await self.build_pil_image(group_id)
            img.save(help_image)

    async def build_html_image(self, group_id: Optional[int]) -> bytes:
        self.sort_type()
        classify = {}
        for menu in self._sort_data:
            for plugin in self._sort_data[menu]:
                sta = 0
                if not plugin.plugin_status.status:
                    if group_id and plugin.plugin_status.block_type in ['all', 'group']:
                        sta = 2
                    if not group_id and plugin.plugin_status.block_type in ['all', 'private']:
                        sta = 2
                if group_id and not group_manager.get_plugin_super_status(plugin.model, group_id):
                    sta = 2
                if group_id and not group_manager.get_plugin_status(plugin.model, group_id):
                    sta = 1
                if classify.get(menu):
                    classify[menu].append(Item(plugin_name=plugin.name, sta=sta))
                else:
                    classify[menu] = [Item(plugin_name=plugin.name, sta=sta)]
        max_len = 0
        flag_index = -1
        max_data = None
        plugin_list = []
        for index, plu in enumerate(classify.keys()):
            if plu in self.icon2str.keys():
                icon = self.icon2str[plu]
            else:
                icon = 'fa fa-pencil-square-o'
            logo = LOGO_PATH / random.choice(os.listdir(LOGO_PATH))
            # print(str(logo.absolute()))
            data = {'name': plu if plu != 'normal' else '功能', 'items': classify[plu], 'icon': icon,
                    'logo': str(logo.absolute())}
            if len(classify[plu]) > max_len:
                max_len = len(classify[plu])
                flag_index = index
                max_data = data
            plugin_list.append(data)
        del plugin_list[flag_index]
        plugin_list.insert(0, max_data)
        pic = await template_to_pic(
            template_path=str((TEMPLATE_PATH / 'menu').absolute()),
            template_name='zhenxun_menu.html',
            templates={"plugin_list": plugin_list},
            pages={
                "viewport": {"width": 1903, "height": 975},
                "base_url": f"file://{TEMPLATE_PATH}",
            },
            wait=2,
        )
        return pic

    async def build_pil_image(self, group_id: Optional[int]) -> BuildImage:
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
