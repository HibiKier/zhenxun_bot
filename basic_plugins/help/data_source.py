from utils.image_utils import BuildImage
from configs.path_config import IMAGE_PATH
from utils.manager import (
    plugins2settings_manager,
    admin_manager,
    plugins_manager,
    group_manager,
)
from typing import Optional
from services.log import logger
from pathlib import Path
from utils.utils import get_matchers
import random
import asyncio
import nonebot
import os


random_bk_path = IMAGE_PATH / "background" / "help" / "simple_help"

background = IMAGE_PATH / "background" / "0.png"


async def create_help_img(
    group_id: Optional[int], help_image: Path, simple_help_image: Path
):
    """
    生成帮助图片
    :param group_id: 群号
    :param help_image: 图片路径
    :param simple_help_image: 简易帮助图片路径
    """
    return await asyncio.get_event_loop().run_in_executor(
        None, _create_help_img, group_id, help_image, simple_help_image
    )


def _create_help_img(
    group_id: Optional[int], help_image: Path, simple_help_image: Path
):
    """
    生成帮助图片
    :param group_id: 群号
    :param help_image: 图片路径
    :param simple_help_image: 简易帮助图片路径
    """
    _matchers = get_matchers()
    width = 0
    matchers_data = {}
    _des_tmp = {}
    _plugin_name_tmp = []
    _tmp = []
    tmp_img = BuildImage(0, 0, plain_text="1", font_size=24)
    font_height = tmp_img.h
    # 插件分类
    for matcher in _matchers:
        plugin_name = None
        _plugin = nonebot.plugin.get_plugin(matcher.plugin_name)
        _module = _plugin.module
        try:
            plugin_name = _module.__getattribute__("__zx_plugin_name__")
            try:
                plugin_des = _module.__getattribute__("__plugin_des__")
            except AttributeError:
                plugin_des = "_"
            if (
                "[hidden]" in plugin_name.lower()
                or "[admin]" in plugin_name.lower()
                or "[superuser]" in plugin_name.lower()
                or plugin_name in _plugin_name_tmp
                or plugin_name == "帮助"
            ):
                continue
            plugin_type = ("normal",)
            text_type = 0
            if plugins2settings_manager.get(
                matcher.plugin_name
            ) and plugins2settings_manager[matcher.plugin_name].get("plugin_type"):
                plugin_type = tuple(
                    plugins2settings_manager.get_plugin_data(matcher.plugin_name)[
                        "plugin_type"
                    ]
                )
            else:
                try:
                    plugin_type = _module.__getattribute__("__plugin_type__")
                except AttributeError:
                    pass
            if len(plugin_type) > 1:
                try:
                    text_type = int(plugin_type[1])
                except ValueError as e:
                    logger.warning(f"生成列向帮助排列失败 {plugin_name}: {type(e)}: {e}")
                plugin_type = plugin_type[0]
            else:
                plugin_type = plugin_type[0]
            try:
                plugin_cmd = _module.__getattribute__("__plugin_cmd__")
                plugin_cmd = [x for x in plugin_cmd if "[_superuser]" not in x]
            except AttributeError:
                plugin_cmd = []
            if plugin_type not in matchers_data.keys():
                matchers_data[plugin_type] = {}
            if plugin_des in _des_tmp.keys():
                try:
                    matchers_data[plugin_type][_des_tmp[plugin_des]]["cmd"] = (
                        matchers_data[plugin_type][_des_tmp[plugin_des]]["cmd"]
                        + plugin_cmd
                    )
                except KeyError as e:
                    logger.warning(f"{type(e)}: {e}")
            else:
                matchers_data[plugin_type][plugin_name] = {
                    "modules": matcher.plugin_name,
                    "des": plugin_des,
                    "cmd": plugin_cmd,
                    "text_type": text_type,
                }
            try:
                if text_type == 0:
                    x = tmp_img.getsize(
                        f'{plugin_name}: {matchers_data[plugin_type][plugin_name]["des"]} ->'
                        + " / ".join(matchers_data[plugin_type][plugin_name]["cmd"])
                    )[0]
                    width = width if width > x else x
            except KeyError:
                pass
            if plugin_des not in _des_tmp:
                _des_tmp[plugin_des] = plugin_name
        except AttributeError as e:
            if plugin_name not in _plugin_name_tmp:
                logger.warning(f"获取功能 {matcher.plugin_name}: {plugin_name} 设置失败...e：{e}")
        if plugin_name not in _plugin_name_tmp:
            _plugin_name_tmp.append(plugin_name)
    help_img_list = []
    simple_help_img_list = []
    types = list(matchers_data.keys())
    types.sort()
    ix = 0
    # 详细帮助
    for type_ in types:
        keys = list(matchers_data[type_].keys())
        keys.sort()
        help_str = f"{type_ if type_ != 'normal' else '功能'}:\n\n"
        simple_help_str = f"{type_ if type_ != 'normal' else '功能'}:\n\n"
        for i, k in enumerate(keys):
            # 禁用flag
            flag = True
            if plugins_manager.get_plugin_status(
                matchers_data[type_][k]["modules"], "all"
            ):
                flag = False
            if group_id:
                flag = flag and plugins_manager.get_plugin_status(
                    matchers_data[type_][k]["modules"], "group"
                )
            simple_help_str += (
                f"{i+1}.{k}<|_|~|>"
                f"{group_manager.get_plugin_status(matchers_data[type_][k]['modules'], group_id) if group_id else '_'}|"
                f"{flag}\n"
            )
            if matchers_data[type_][k]["text_type"] == 1:
                _x = tmp_img.getsize(
                    f"{i+1}".rjust(5)
                    + f'.{k}: {matchers_data[type_][k]["des"]} {"->" if matchers_data[type_][k]["cmd"] else ""} '
                )[0]
                _str = (
                    f"{i+1}".rjust(5)
                    + f'.{k}: {matchers_data[type_][k]["des"]} {"->" if matchers_data[type_][k]["cmd"] else ""} '
                )
                _str += matchers_data[type_][k]["cmd"][0] + "\n"
                for c in matchers_data[type_][k]["cmd"][1:]:
                    _str += "".rjust(int(_x * 0.125) + 1) + f"{c}\n"
                help_str += _str
            else:
                help_str += (
                    f"{i+1}".rjust(5)
                    + f'.{k}: {matchers_data[type_][k]["des"]} {"->" if matchers_data[type_][k]["cmd"] else ""} '
                    + " / ".join(matchers_data[type_][k]["cmd"])
                    + "\n"
                )
        height = len(help_str.split("\n")) * (font_height + 5)
        simple_height = len(simple_help_str.split("\n")) * (font_height + 5)
        A = BuildImage(
            width + 150, height, font_size=24, color="white" if not ix % 2 else "black"
        )
        A.text((10, 10), help_str, (255, 255, 255) if ix % 2 else (0, 0, 0))
        # 生成各个分类的插件简易帮助图片
        simple_width = 0
        for x in [
            tmp_img.getsize(x.split("<|_|~|>")[0])[0]
            for x in simple_help_str.split("\n")
        ]:
            simple_width = simple_width if simple_width > x else x
        bk = BuildImage(simple_width + 20, simple_height, font_size=24, color="#6495ED")
        B = BuildImage(
            simple_width + 20,
            simple_height,
            font_size=24,
            color="white" if not ix % 2 else "black",
        )
        # 切分，判断插件开关状态
        _s_height = 10
        for _s in simple_help_str.split("\n"):
            text_color = (255, 255, 255) if ix % 2 else (0, 0, 0)
            _line_flag = False
            if "<|_|~|>" in _s:
                _x = _s.split("<|_|~|>")
                _flag_sp = _x[-1].split("|")
                if group_id:
                    if _flag_sp[0].lower() != "true":
                        text_color = (252, 75, 13)
                if _flag_sp[1].lower() == "true":
                    _line_flag = True
                _s = _x[0]
            B.text((10, _s_height), _s, text_color)
            if _line_flag:
                B.line(
                    (
                        7,
                        _s_height + int(B.getsize(_s)[1] / 2) + 2,
                        B.getsize(_s)[0] + 11,
                        _s_height + int(B.getsize(_s)[1] / 2) + 2,
                    ),
                    (236, 66, 7),
                    3,
                )
            _s_height += B.getsize("1")[1] + 5
        # B.text((10, 10), simple_help_str, (255, 255, 255) if ix % 2 else (0, 0, 0))
        bk.paste(B, center_type="center")
        bk.transparent(2)
        ix += 1
        help_img_list.append(A)
        simple_help_img_list.append(bk)
    height = 0
    for img in help_img_list:
        height += img.h
    if not group_id:
        A = BuildImage(width + 150, height + 50, font_size=24)
        A.text(
            (10, 10), '*  注: ‘*’ 代表可有多个相同参数 ‘?’ 代表可省略该参数  *\n\n" "功能名: 功能简介 -> 指令\n\n'
        )
        current_height = 50
        for img in help_img_list:
            A.paste(img, (0, current_height))
            current_height += img.h
        A.save(help_image)
    # 详细帮助生成完毕
    # 简易帮助图片合成
    height = 0
    width = 0
    for img in simple_help_img_list:
        if img.h > height:
            height = img.h
        width += img.w + 10
    B = BuildImage(width + 100, height + 250, font_size=24)
    width, _ = get_max_width_or_paste(simple_help_img_list, B)
    bk = None
    random_bk = os.listdir(random_bk_path)
    if random_bk:
        bk = random.choice(random_bk)
    x = max(width + 50, height + 250)
    B = BuildImage(
        x,
        x,
        font_size=24,
        color="#FFEFD5",
        background=random_bk_path / bk,
    )
    B.filter("GaussianBlur", 10)
    _, B = get_max_width_or_paste(simple_help_img_list, B, True)
    w = 10
    h = 10
    for msg in ["目前支持的功能列表:", "可以通过 ‘帮助[功能名称]’ 来获取对应功能的使用方法", "或者使用 ‘详细帮助’ 来获取所有功能方法"]:
        text = BuildImage(
            0,
            0,
            plain_text=msg,
            font_size=24,
            font="yuanshen.ttf",
        )
        B.paste(text, (w, h), True)
        h += 50
        if msg == "目前支持的功能列表:":
            w += 50
    B.paste(
        BuildImage(
            0,
            0,
            plain_text="注: 红字代表功能被群管理员禁用，红线代表功能正在维护",
            font_size=24,
            font="yuanshen.ttf",
            font_color=(231, 74, 57)
        ),
        (300, 10),
        True,
    )
    B.save(simple_help_image)


def get_max_width_or_paste(
    simple_help_img_list: list, B: BuildImage = None, is_paste: bool = False
) -> "int, BuildImage":
    """
    获取最大宽度，或直接贴图
    :param simple_help_img_list: 简单帮助图片列表
    :param B: 背景图
    :param is_paste: 是否直接贴图
    """
    current_width = 50
    current_height = 180
    max_width = simple_help_img_list[0].w
    for i in range(len(simple_help_img_list)):
        try:
            if is_paste and B:
                B.paste(simple_help_img_list[i], (current_width, current_height), True)
            current_height += simple_help_img_list[i].h + 40
            if current_height + simple_help_img_list[i + 1].h > B.h - 10:
                current_height = 180
                current_width += max_width + 30
                max_width = 0
            elif simple_help_img_list[i].w > max_width:
                max_width = simple_help_img_list[i].w
        except IndexError:
            pass
    if current_width > simple_help_img_list[0].w + 50:
        current_width += simple_help_img_list[-1].w
    return current_width, B


def get_plugin_help(msg: str, is_super: bool = False) -> Optional[str]:
    """
    获取功能的帮助信息
    :param msg: 功能cmd
    :param is_super: 是否为超级用户
    """
    module = plugins2settings_manager.get_plugin_module(msg)
    if not module:
        module = admin_manager.get_plugin_module(msg)
    if module:
        try:
            plugin = nonebot.plugin.get_plugin(module)
            if plugin:
                if is_super:
                    result = plugin.module.__getattribute__(
                        "__plugin_superuser_usage__"
                    )
                else:
                    result = plugin.module.__getattribute__("__plugin_usage__")
                if result:
                    width = 0
                    for x in result.split("\n"):
                        _width = len(x) * 24
                        width = width if width > _width else _width
                    height = len(result.split("\n")) * 45
                    A = BuildImage(width, height, font_size=24)
                    bk = BuildImage(
                        width,
                        height,
                        background=IMAGE_PATH / "background" / "1.png",
                    )
                    A.paste(bk, alpha=True)
                    A.text((int(width * 0.048), int(height * 0.21)), result)
                    return A.pic2bs4()
        except AttributeError:
            pass
    return None
