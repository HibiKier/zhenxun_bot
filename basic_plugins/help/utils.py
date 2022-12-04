from typing import List, Tuple, Dict, Optional, Union
from configs.path_config import IMAGE_PATH
from utils.image_utils import BuildImage
from pydantic import BaseModel
import os
import random

background_path = IMAGE_PATH / "background" / "help" / "simple_help"

# class PluginType(BaseModel):
#
#
# class Plugin(BaseModel):
#     name: str
#     plugin_type: PluginType                # 插件内部类型，根据name [Hidden] [Admin] [SUPERUSER]
#     usage: Optional[str]
#     des: Optional[str]
#     cmd: Optional[List[str]]
#     task: Optional[Dict[str, str]]
#     type: Optional[Tuple[str, int]]                # 菜单类型
#     version: Optional[Union[str, int]]
#     author: Optional[str]




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


# class HelpImageBuild:
#
#     def __init__(self):
#         self._data: Dict[str, List[]] = {}

