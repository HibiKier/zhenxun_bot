import os
import shutil
import zipfile
from pathlib import Path
from typing import Union, Tuple
from utils.manager import plugins_manager

import ujson as json

from services import logger
from utils.http_utils import AsyncHttpx
from configs.path_config import TEMP_PATH, DATA_PATH
from utils.image_utils import text2image, BuildImage
from utils.utils import is_number

path = DATA_PATH / "plugin_shop"
if not path.exists():
    path.mkdir(parents=True, exist_ok=True)

repo_json_url = "https://github.com/zhenxun-org/nonebot_plugins_zhenxun_bot/archive/refs/heads/index.zip"
repo_zip_path = TEMP_PATH / "plugin_repo_json.zip"
plugin_json = path / "zhenxun_plugins.json"

extensive_plugin_path = Path() / "extensive_plugin"

path = DATA_PATH / "plugin_shop"
if not path.exists():
    path.mkdir(parents=True, exist_ok=True)
if not extensive_plugin_path.exists():
    extensive_plugin_path.mkdir(parents=True, exist_ok=True)

data = {}


async def install_plugin(name: str) -> str:
    """
    安装插件
    :param name: 插件名或下标
    """
    try:
        if is_number(name):
            name, code = await get_plugin_name(int(name))
            if code != 200:
                return name
        plugin_url = data[name]["download_url"]
        url = (await AsyncHttpx.get(plugin_url)).headers.get("Location")
        zip_file = TEMP_PATH / f"{name}.zip"
        if zip_file.exists():
            zip_file.unlink()
        if await AsyncHttpx.download_file(url, zip_file):
            logger.debug("开始解压插件压缩包...")
            # 解压
            zf = zipfile.ZipFile(zip_file, "r")
            extract_path = TEMP_PATH / f"{name}"
            if extract_path.exists():
                shutil.rmtree(extract_path.absolute(), ignore_errors=True)
            extract_path.mkdir(exist_ok=True, parents=True)
            for file in zf.namelist():
                zf.extract(file, extract_path)
            zf.close()
            logger.debug("解压插件压缩包完成...")
            logger.debug("开始移动插件文件夹...")
            if (extensive_plugin_path / f"{name}").exists():
                logger.debug("extensive_plugin目录下文件夹已存在，删除该目录插件文件夹...")
                shutil.rmtree(
                    (extensive_plugin_path / f"{name}").absolute(), ignore_errors=True
                )
            extract_path.rename(extensive_plugin_path / f"{name}")
            tmp = ""
            if "pyproject.toml" in os.listdir(extensive_plugin_path / f"{name}"):
                tmp = "检测到该插件含有额外依赖，当前安装无法保证依赖完全安装成功。"
                os.system(
                    f"poetry run pip install -r {(extensive_plugin_path / f'{name}' / 'pyproject.toml').absolute()}"
                )
            elif "requirements.txt" in os.listdir(extensive_plugin_path / f"{name}"):
                tmp = "检测到该插件含有额外依赖，当前安装无法保证依赖完全安装成功。"
                os.system(
                    f"poetry run pip install -r {(extensive_plugin_path / f'{name}' / 'requirements.txt').absolute()}"
                )
            with open(extensive_plugin_path / f"{name}" / "plugin_info.json", "w") as f:
                json.dump(data[name], f, ensure_ascii=False, indent=4)
            logger.debug("移动插件文件夹完成...")
            logger.info(f"成功安装插件 {name} 成功！\n{tmp}")
        return f"成功安装插件 {name}，请重启真寻！"
    except Exception as e:
        logger.error(f"安装插件 {name} 失败 {type(e)}：{e}")
        return f"安装插件 {name} 失败 {type(e)}：{e}"


async def uninstall_plugin(name: str) -> str:
    """
    删除插件
    :param name: 插件名或下标
    """
    try:
        if is_number(name):
            name, code = await get_plugin_name(int(name))
            if code != 200:
                return name
        if name not in os.listdir(extensive_plugin_path):
            return f"未安装 {name} 插件！"
        shutil.rmtree((extensive_plugin_path / name).absolute(), ignore_errors=True)
        logger.info(f"插件 {name} 删除成功！")
        return f"插件 {name} 删除成功！"
    except Exception as e:
        logger.error(f"删除插件 {name} 失败 {type(e)}：{e}")
        return f"删除插件 {name} 失败 {type(e)}：{e}"


async def show_plugin_repo() -> Union[int, str]:
    """
    获取插件仓库数据并格式化
    """
    if not plugin_json.exists():
        code = await download_json()
        if code != 200:
            return code
    plugin_info = json.load(open(plugin_json, "r", encoding="utf8"))
    load_plugin_list = plugins_manager.get_data().keys()
    image_list = []
    w, h = 0, 0
    line_height = 10
    for i, key in enumerate(plugin_info.keys()):
        data[key] = {
            "名称": plugin_info[key]["plugin_name"],
            "模块": key,
            "作者": plugin_info[key]["author"],
            "版本": plugin_info[key]["version"],
            "简介": plugin_info[key]["introduction"],
            "download_url": plugin_info[key]["download_url"],
            "github_url": plugin_info[key]["github_url"],
        }
        status = ""
        version = ""
        if key in load_plugin_list:
            status = "<f font_color=#1a7e30>[已安装]</f>"
            version = f"<f font_color=#1a7e30>[{plugins_manager.get_data()[key]['version']}]</f>"
        s = (
            f'id：{i+1}\n名称：{plugin_info[key]["plugin_name"]}'
            f' \t\t{status}\n'
            f"模块：{key}\n"
            f'作者：{plugin_info[key]["author"]}\n'
            f'版本：{plugin_info[key]["version"]} \t\t{version}\n'
            f'简介：{plugin_info[key]["introduction"]}\n'
            f"-------------------"
        )
        img = await text2image(s, font_size=20, color="#f9f6f2")
        w = w if w > img.w else img.w
        h += img.h + line_height
        image_list.append(img)
    A = BuildImage(w + 50, h + 50, color="#f9f6f2")
    cur_h = 25
    for img in image_list:
        await A.apaste(img, (25, cur_h))
        cur_h += img.h + line_height
    return A.pic2bs4()


async def download_json() -> int:
    """
    下载插件库json文件
    """
    try:
        url = (await AsyncHttpx.get(repo_json_url)).headers.get("Location")
        if repo_zip_path.exists():
            repo_zip_path.unlink()
        if await AsyncHttpx.download_file(url, repo_zip_path):
            zf = zipfile.ZipFile(repo_zip_path, "r")
            extract_path = path / "temp"
            for file in zf.namelist():
                zf.extract(file, extract_path)
            zf.close()
            if plugin_json.exists():
                plugin_json.unlink()
            (
                extract_path
                / "nonebot_plugins_zhenxun_bot-index"
                / "zhenxun_plugins.json"
            ).rename(plugin_json)
            shutil.rmtree(extract_path.absolute(), ignore_errors=True)
            return 200
    except Exception as e:
        logger.error(f"下载插件库压缩包失败或解压失败 {type(e)}：{e}")
    return 999


async def get_plugin_name(name: int) -> Tuple[str, int]:
    """
    通过下标获取插件名
    :param name: 下标
    """
    name = int(name)
    if not data:
        await show_plugin_repo()
    if name < 1 or name > len(data.keys()):
        return "下标超过上下限！", 999
    name = list(data.keys())[name - 1]
    return name, 200
