from typing import Tuple, Optional, List
from configs.path_config import IMAGE_PATH, TEXT_PATH
from PIL.Image import UnidentifiedImageError
from utils.message_builder import image
from services.log import logger
from utils.image_utils import BuildImage
from asyncio.exceptions import TimeoutError
from asyncio import Semaphore
from utils.image_utils import is_valid
from utils.http_utils import AsyncHttpx
from httpx import ConnectTimeout
from .map import Map
import asyncio
import nonebot
import os

try:
    import ujson as json
except ModuleNotFoundError:
    import json

driver: nonebot.Driver = nonebot.get_driver()

LABEL_URL = "https://api-static.mihoyo.com/common/blackboard/ys_obc/v1/map/label/tree?app_sn=ys_obc"
POINT_LIST_URL = "https://api-static.mihoyo.com/common/blackboard/ys_obc/v1/map/point/list?map_id=2&app_sn=ys_obc"
MAP_URL = "https://api-static.mihoyo.com/common/map_user/ys_obc/v1/map/info?map_id=2&app_sn=ys_obc&lang=zh-cn"

icon_path = IMAGE_PATH / "genshin" / "genshin_icon"
map_path = IMAGE_PATH / "genshin" / "map"
resource_label_file = TEXT_PATH / "genshin" / "resource_label_file.json"
resource_point_file = TEXT_PATH / "genshin" / "resource_point_file.json"
resource_type_file = TEXT_PATH / "genshin" / "resource_type_file.json"

# 地图中心坐标
CENTER_POINT: Optional[Tuple[int, int]] = None

resource_name_list: List[str] = []

MAP_RATIO = 0.5


# 查找资源
async def query_resource(resource_name: str) -> str:
    global CENTER_POINT
    planning_route: bool = False
    if resource_name and resource_name[-2:] in ["路径", "路线"]:
        resource_name = resource_name[:-2].strip()
        planning_route = True
    if not resource_name or resource_name not in resource_name_list:
        # return f"未查找到 {resource_name} 资源，可通过 “原神资源列表” 获取全部资源名称.."
        return ""
    map_ = Map(
        resource_name, CENTER_POINT, planning_route=planning_route, ratio=MAP_RATIO
    )
    count = map_.get_resource_count()
    rand = await asyncio.get_event_loop().run_in_executor(
        None, map_.generate_resource_icon_in_map
    )
    return (
        f"{image(f'genshin_map_{rand}.png', 'temp')}"
        f"\n\n※ {resource_name} 一共找到 {count} 个位置点\n※ 数据来源于米游社wiki"
    )


# 原神资源列表
def get_resource_type_list():
    with open(resource_type_file, "r", encoding="utf8") as f:
        data = json.load(f)
    temp = {}
    for id_ in data.keys():
        temp[data[id_]["name"]] = []
        for x in data[id_]["children"]:
            temp[data[id_]["name"]].append(x["name"])

    mes = "当前资源列表如下：\n"

    for resource_type in temp.keys():
        mes += f"{resource_type}：{'，'.join(temp[resource_type])}\n"
    return mes


def check_resource_exists(resource: str) -> bool:
    """
    检查资源是否存在
    :param resource: 资源名称
    """
    resource = resource.replace("路径", "").replace("路线", "")
    return resource in resource_name_list


@driver.on_startup
async def init(flag: bool = False):
    global CENTER_POINT, resource_name_list
    try:
        semaphore = asyncio.Semaphore(10)
        await download_map_init(semaphore, flag)
        await download_resource_data(semaphore)
        await download_resource_type()
        if not CENTER_POINT:
            if resource_label_file.exists():
                CENTER_POINT = json.load(
                    open(resource_label_file, "r", encoding="utf8")
                )["CENTER_POINT"]
        if resource_label_file.exists():
            with open(resource_type_file, "r", encoding="utf8") as f:
                data = json.load(f)
            for id_ in data:
                for x in data[id_]["children"]:
                    resource_name_list.append(x["name"])
    except TimeoutError:
        logger.warning("原神资源查询信息初始化超时....")


# 图标及位置资源
async def download_resource_data(semaphore: Semaphore):
    icon_path.mkdir(parents=True, exist_ok=True)
    resource_label_file.parent.mkdir(parents=True, exist_ok=True)
    try:
        response = await AsyncHttpx.get(POINT_LIST_URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data["message"] == "OK":
                data = data["data"]
                for lst in ["label_list", "point_list"]:
                    resource_data = {"CENTER_POINT": CENTER_POINT}
                    tasks = []
                    file = (
                        resource_label_file
                        if lst == "label_list"
                        else resource_point_file
                    )
                    for x in data[lst]:
                        id_ = x["id"]
                        if lst == "label_list":
                            img_url = x["icon"]
                            tasks.append(
                                asyncio.ensure_future(
                                    download_image(
                                        img_url,
                                        f"{icon_path}/{id_}.png",
                                        semaphore,
                                        True,
                                    )
                                )
                            )
                        resource_data[id_] = x
                    await asyncio.gather(*tasks)
                    with open(file, "w", encoding="utf8") as f:
                        json.dump(resource_data, f, ensure_ascii=False, indent=4)
            else:
                logger.warning(f'获取原神资源失败 msg: {data["message"]}')
        else:
            logger.warning(f"获取原神资源失败 code：{response.status_code}")
    except (TimeoutError, ConnectTimeout):
        logger.warning("获取原神资源数据超时...已再次尝试...")
        await download_resource_data(semaphore)
    except Exception as e:
        logger.error(f"获取原神资源数据未知错误 {type(e)}：{e}")


# 下载原神地图并拼图
async def download_map_init(semaphore: Semaphore, flag: bool = False):
    global CENTER_POINT, MAP_RATIO
    map_path.mkdir(exist_ok=True, parents=True)
    _map = map_path / "map.png"
    if _map.exists() and os.path.getsize(_map) > 1024 * 1024 * 30:
        _map.unlink()
    try:
        response = await AsyncHttpx.get(MAP_URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data["message"] == "OK":
                data = json.loads(data["data"]["info"]["detail"])
                CENTER_POINT = (data["origin"][0], data["origin"][1])
                if not _map.exists():
                    data = data["slices"]
                    idx = 0
                    for _map_data in data[0]:
                        map_url = _map_data["url"]
                        await download_image(
                            map_url,
                            f"{map_path}/{idx}.png",
                            semaphore,
                            force_flag=flag,
                        )
                        BuildImage(
                            0, 0, background=f"{map_path}/{idx}.png", ratio=MAP_RATIO
                        ).save()
                        idx += 1
                    _w, h = BuildImage(0, 0, background=f"{map_path}/0.png").size
                    w = _w * len(os.listdir(map_path))
                    map_file = BuildImage(w, h, _w, h, ratio=MAP_RATIO)
                    for i in range(idx):
                        map_file.paste(
                            BuildImage(0, 0, background=f"{map_path}/{i}.png")
                        )
                    map_file.save(f"{map_path}/map.png")
            else:
                logger.warning(f'获取原神地图失败 msg: {data["message"]}')
        else:
            logger.warning(f"获取原神地图失败 code：{response.status_code}")
    except (TimeoutError, ConnectTimeout):
        logger.warning("下载原神地图数据超时....")
    except Exception as e:
        logger.error(f"下载原神地图数据超时 {type(e)}：{e}")


# 下载资源类型数据
async def download_resource_type():
    resource_type_file.parent.mkdir(parents=True, exist_ok=True)
    try:
        response = await AsyncHttpx.get(LABEL_URL, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data["message"] == "OK":
                data = data["data"]["tree"]
                resource_data = {}
                for x in data:
                    id_ = x["id"]
                    resource_data[id_] = x
                with open(resource_type_file, "w", encoding="utf8") as f:
                    json.dump(resource_data, f, ensure_ascii=False, indent=4)
                logger.info(f"更新原神资源类型成功...")
            else:
                logger.warning(f'获取原神资源类型失败 msg: {data["message"]}')
        else:
            logger.warning(f"获取原神资源类型失败 code：{response.status_code}")
    except (TimeoutError, ConnectTimeout):
        logger.warning("下载原神资源类型数据超时....")
    except Exception as e:
        logger.error(f"载原神资源类型数据超时 {type(e)}：{e}")


# 初始化资源图标
def gen_icon(icon: str):
    A = BuildImage(0, 0, background=f"{icon_path}/box.png")
    B = BuildImage(0, 0, background=f"{icon_path}/box_alpha.png")
    icon_ = icon_path / f"{icon}"
    icon_img = BuildImage(115, 115, background=icon_)
    icon_img.circle()
    B.paste(icon_img, (17, 10), True)
    B.paste(A, alpha=True)
    B.save(icon)
    logger.info(f"生成图片成功 file：{str(icon)}")


# 下载图片
async def download_image(
    img_url: str,
    path: str,
    semaphore: Semaphore,
    gen_flag: bool = False,
    force_flag: bool = False,
):
    async with semaphore:
        try:
            if not os.path.exists(path) or not is_valid or force_flag:
                if await AsyncHttpx.download_file(img_url, path, timeout=10):
                    logger.info(f"下载原神资源图标：{img_url}")
                    if gen_flag:
                        gen_icon(path)
                else:
                    logger.info(f"下载原神资源图标：{img_url} 失败，等待下次更新...")
        except UnidentifiedImageError:
            logger.warning(f"原神图片打开错误..已删除，等待下次更新... file: {path}")
            if os.path.exists(path):
                os.remove(path)


#
# def _get_point_ratio():
#
