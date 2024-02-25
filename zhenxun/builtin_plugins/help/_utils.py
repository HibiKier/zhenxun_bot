import os
import random
from typing import Dict

from zhenxun.configs.config import Config
from zhenxun.configs.path_config import DATA_PATH, IMAGE_PATH, TEMPLATE_PATH
from zhenxun.models.group_console import GroupConsole
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.utils.enum import BlockType, PluginType
from zhenxun.utils.image_utils import BuildImage, build_sort_image, group_image

from ._config import Item

GROUP_HELP_PATH = DATA_PATH / "group_help"
GROUP_HELP_PATH.mkdir(exist_ok=True, parents=True)
for f in os.listdir(GROUP_HELP_PATH):
    group_help_image = GROUP_HELP_PATH / f
    group_help_image.unlink()

BACKGROUND_PATH = IMAGE_PATH / "background" / "help" / "simple_help"

LOGO_PATH = TEMPLATE_PATH / "menu" / "res" / "logo"


class HelpImageBuild:
    def __init__(self):
        self._data: list[PluginInfo] = []
        self._sort_data: Dict[str, list[PluginInfo]] = {}
        self._image_list = []
        self.icon2str = {
            "normal": "fa fa-cog",
            "原神相关": "fa fa-circle-o",
            "常规插件": "fa fa-cubes",
            "联系管理员": "fa fa-envelope-o",
            "抽卡相关": "fa fa-credit-card-alt",
            "来点好康的": "fa fa-picture-o",
            "数据统计": "fa fa-bar-chart",
            "一些工具": "fa fa-shopping-cart",
            "商店": "fa fa-shopping-cart",
            "其它": "fa fa-tags",
            "群内小游戏": "fa fa-gamepad",
        }

    async def sort_type(self):
        """
        对插件按照菜单类型分类
        """
        if not self._data:
            self._data = await PluginInfo.filter(plugin_type=PluginType.NORMAL)
        if not self._sort_data:
            for plugin in self._data:
                menu_type = plugin.menu_type or "normal"
                if not self._sort_data.get(menu_type):
                    self._sort_data[menu_type] = []
                self._sort_data[menu_type].append(plugin)

    async def build_image(self, group_id: int | None):
        if group_id:
            help_image = GROUP_HELP_PATH / f"{group_id}.png"
        else:
            help_image = IMAGE_PATH / f"SIMPLE_HELP.png"
        build_type = Config.get_config("help", "TYPE")
        if build_type == "HTML":
            byt = await self.build_html_image(group_id)
            with open(help_image, "wb") as f:
                f.write(byt)
        else:
            img = await self.build_pil_image(group_id)
            await img.save(help_image)

    async def build_html_image(self, group_id: int | None) -> bytes:
        from nonebot_plugin_htmlrender import template_to_pic

        await self.sort_type()
        classify = {}
        for menu in self._sort_data:
            for plugin in self._sort_data[menu]:
                sta = 0
                if not plugin.status:
                    if group_id and plugin.block_type in [
                        BlockType.ALL,
                        BlockType.GROUP,
                    ]:
                        sta = 2
                    if not group_id and plugin.block_type in [
                        BlockType.ALL,
                        BlockType.PRIVATE,
                    ]:
                        sta = 2
                if group_id and (
                    group := await GroupConsole.get_or_none(group_id=group_id)
                ):
                    if f"{plugin.module}:super," in group.block_plugin:
                        sta = 2
                    if f"{plugin.module}," in group.block_plugin:
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
                icon = "fa fa-pencil-square-o"
            logo = LOGO_PATH / random.choice(os.listdir(LOGO_PATH))
            data = {
                "name": plu if plu != "normal" else "功能",
                "items": classify[plu],
                "icon": icon,
                "logo": str(logo.absolute()),
            }
            if len(classify[plu]) > max_len:
                max_len = len(classify[plu])
                flag_index = index
                max_data = data
            plugin_list.append(data)
        del plugin_list[flag_index]
        plugin_list.insert(0, max_data)
        pic = await template_to_pic(
            template_path=str((TEMPLATE_PATH / "menu").absolute()),
            template_name="zhenxun_menu.html",
            templates={"plugin_list": plugin_list},
            pages={
                "viewport": {"width": 1903, "height": 975},
                "base_url": f"file://{TEMPLATE_PATH}",
            },
            wait=2,
        )
        return pic

    async def build_pil_image(self, group_id: int | None) -> BuildImage:
        """构造帮助图片

        参数:
             group_id: 群号
        """
        self._image_list = []
        await self.sort_type()
        font_size = 24
        build_type = Config.get_config("help", "TYPE")
        _image = BuildImage.build_text_image("1", size=font_size)
        font = BuildImage.load_font("HYWenHei-85W.ttf", 20)
        for idx, menu_type in enumerate(self._sort_data.keys()):
            plugin_list = self._sort_data[menu_type]
            wh_list = [BuildImage.get_text_size(x.name, font) for x in plugin_list]
            wh_list.append(BuildImage.get_text_size(menu_type, font))
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
            if group := await GroupConsole.get_or_none(group_id=group_id):
                for i, plugin in enumerate(plugin_list):
                    text_color = (255, 255, 255) if idx % 2 else (0, 0, 0)
                    if f"{plugin.module}," in group.block_plugin:
                        text_color = (252, 75, 13)
                    pos = None
                    # 禁用状态划线
                    if (
                        plugin.block_type in [BlockType.ALL, BlockType.GROUP]
                        or f"{plugin.module}:super," in group.block_plugin
                    ):
                        w = curr_h + int(B.getsize(plugin.name)[1] / 2) + 2
                        pos = (
                            7,
                            w,
                            B.getsize(plugin.name)[0] + 35,
                            w,
                        )
                    if build_type == "VV":
                        name_image = await self.build_name_image(  # type: ignore
                            max_width,
                            plugin.name,
                            "black" if not idx % 2 else "white",
                            text_color,
                            pos,
                        )
                        await B.paste(name_image, (0, curr_h), center_type="width")
                        curr_h += name_image.h + 5
                    else:
                        await B.text((10, curr_h), f"{i + 1}.{plugin.name}", text_color)
                        if pos:
                            await B.line(pos, (236, 66, 7), 3)
                        curr_h += font_size + 5
            if menu_type == "normal":
                menu_type = "功能"
            await bk.text((0, 14), menu_type, center_type="width")
            await bk.paste(B, (0, 50))
            await bk.transparent(2)
            # await bk.acircle_corner(point_list=['lt', 'rt'])
            self._image_list.append(bk)
        image_group, h = group_image(self._image_list)
        B = await build_sort_image(
            image_group,
            h,
            background_path=BACKGROUND_PATH,
            background_handle=lambda image: image.filter("GaussianBlur", 5),
        )
        w = 10
        h = 10
        for msg in [
            "目前支持的功能列表:",
            "可以通过 ‘帮助[功能名称]’ 来获取对应功能的使用方法",
        ]:
            text = await BuildImage.build_text_image(msg, "HYWenHei-85W.ttf", 24)
            await B.paste(text, (w, h))
            h += 50
            if msg == "目前支持的功能列表:":
                w += 50
        text = await BuildImage.build_text_image(
            "注: 红字代表功能被群管理员禁用，红线代表功能正在维护",
            "HYWenHei-85W.ttf",
            24,
            (231, 74, 57),
        )
        await B.paste(
            text,
            (300, 10),
        )
        return B
