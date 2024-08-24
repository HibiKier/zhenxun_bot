import os
import shutil
import subprocess
from pathlib import Path

import nonebot
import ujson as json

from zhenxun.services.log import logger
from zhenxun.utils.http_utils import AsyncHttpx
from zhenxun.utils.image_utils import BuildImage, ImageTemplate, RowStyle

from .config import BASE_PATH, CONFIG_URL, DOWNLOAD_URL


def row_style(column: str, text: str) -> RowStyle:
    """被动技能文本风格

    参数:
        column: 表头
        text: 文本内容

    返回:
        RowStyle: RowStyle
    """
    style = RowStyle()
    if column in ["-"]:
        if text == "已安装":
            style.font_color = "#67C23A"
    return style


async def recurrence_get_url(
    url: str, data_list: list[tuple[str, str]], ignore_list: list[str] = []
):
    """递归获取目录下所有文件

    参数:
        url: 信息url
        data_list: 数据列表

    异常:
        ValueError: 访问错误
    """
    logger.debug(f"访问插件下载信息 URL: {url}", "插件管理")
    res = await AsyncHttpx.get(url)
    if res.status_code != 200:
        raise ValueError(f"访问错误, code: {res.status_code}")
    json_data = res.json()
    if isinstance(json_data, list):
        for v in json_data:
            data_list.append((v.get("download_url"), v["path"]))
    else:
        data_list.append((json_data.get("download_url"), json_data["path"]))
    for download_url, path in data_list:
        if not download_url:
            _url = DOWNLOAD_URL.format(path)
            if _url not in ignore_list:
                ignore_list.append(_url)
                await recurrence_get_url(_url, data_list, ignore_list)


async def download_file(url: str):
    """下载文件

    参数:
        url: 插件详情url

    异常:
        ValueError: 访问失败
        ValueError: 下载失败
    """
    data_list = []
    await recurrence_get_url(url, data_list)
    for download_url, path in data_list:
        if download_url and "." in path:
            logger.debug(f"下载文件: {path}", "插件管理")
            file = Path(f"zhenxun/{path}")
            file.parent.mkdir(parents=True, exist_ok=True)
            r = await AsyncHttpx.get(download_url)
            if r.status_code != 200:
                raise ValueError(f"文件下载错误, code: {r.status_code}")
            with open(file, "w", encoding="utf8") as f:
                logger.debug(f"写入文件: {file}", "插件管理")
                f.write(r.text)


def install_requirement(plugin_path: Path):
    requirement_path = plugin_path / "requirement.txt"

    if not requirement_path.exists():
        logger.debug(
            f"No requirement.txt found for plugin: {plugin_path.name}", "插件管理"
        )
        return

    try:
        result = subprocess.run(
            ["pip", "install", "-r", str(requirement_path)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        logger.debug(
            f"Successfully installed dependencies for plugin: {plugin_path.name}. Output:\n{result.stdout}",
            "插件管理",
        )
    except subprocess.CalledProcessError as e:
        logger.error(
            f"Failed to install dependencies for plugin: {plugin_path.name}. Error:\n{e.stderr}"
        )


class ShopManage:

    type2name = {
        "NORMAL": "普通插件",
        "ADMIN": "管理员插件",
        "SUPERUSER": "超级用户插件",
        "ADMIN_SUPERUSER": "管理员/超级用户插件",
        "DEPENDANT": "依赖插件",
        "HIDDEN": "其他插件",
    }

    @classmethod
    async def __get_data(cls) -> dict:
        """获取插件信息数据

        异常:
            ValueError: 访问请求失败

        返回:
            dict: 插件信息数据
        """
        res = await AsyncHttpx.get(CONFIG_URL)
        if res.status_code != 200:
            raise ValueError(f"下载错误, code: {res.status_code}")
        return json.loads(res.text)

    @classmethod
    async def get_plugins_info(cls) -> BuildImage | str:
        """插件列表

        返回:
            BuildImage | str: 返回消息
        """
        data: dict = await cls.__get_data()
        column_name = ["-", "ID", "名称", "简介", "作者", "版本", "类型"]
        for k in data.copy():
            if data[k]["plugin_type"]:
                data[k]["plugin_type"] = cls.type2name[data[k]["plugin_type"]]
        suc_plugin = [p.name for p in nonebot.get_loaded_plugins()]
        data_list = [
            [
                "已安装" if v[1]["module"] in suc_plugin else "",
                i,
                v[0],
                v[1]["description"],
                v[1]["author"],
                v[1]["version"],
                v[1]["plugin_type"],
            ]
            for i, v in enumerate(data.items())
        ]
        return await ImageTemplate.table_page(
            "插件列表",
            f"通过安装/卸载插件 ID 来管理插件",
            column_name,
            data_list,
            text_style=row_style,
        )

    @classmethod
    async def add_plugin(cls, plugin_id: int) -> str:
        data: dict = await cls.__get_data()
        if plugin_id < 0 or plugin_id >= len(data):
            return "插件ID不存在..."
        plugin_key = list(data.keys())[plugin_id]
        plugin_info = data[plugin_key]
        module_path_split = plugin_info["module_path"].split(".")
        url_path = None
        path = BASE_PATH
        if len(module_path_split) == 2:
            """单个文件或文件夹"""
            if plugin_info["is_dir"]:
                url_path = "/".join(module_path_split)
            else:
                url_path = "/".join(module_path_split) + ".py"
        else:
            """嵌套文件或文件夹"""
            for p in module_path_split[:-1]:
                path = path / p
            path.mkdir(parents=True, exist_ok=True)
            if plugin_info["is_dir"]:
                url_path = f"{'/'.join(module_path_split)}"
            else:
                url_path = f"{'/'.join(module_path_split)}.py"
        if not url_path:
            return "插件下载地址构建失败..."
        logger.debug(f"尝试下载插件 URL: {url_path}", "插件管理")
        await download_file(DOWNLOAD_URL.format(url_path))

        # 安装依赖
        plugin_path = BASE_PATH / "/".join(module_path_split)
        install_requirement(plugin_path)

        return f"插件 {plugin_key} 安装成功!"

    @classmethod
    async def remove_plugin(cls, plugin_id: int) -> str:
        data: dict = await cls.__get_data()
        if plugin_id < 0 or plugin_id >= len(data):
            return "插件ID不存在..."
        plugin_key = list(data.keys())[plugin_id]
        plugin_info = data[plugin_key]
        path = BASE_PATH
        for p in plugin_info["module_path"].split("."):
            path = path / p
        if not plugin_info["is_dir"]:
            path = Path(f"{path}.py")
        if not path.exists():
            return f"插件 {plugin_key} 不存在..."
        logger.debug(f"尝试移除插件 {plugin_key} 文件: {path}", "插件管理")
        if plugin_info["is_dir"]:
            shutil.rmtree(path)
        else:
            path.unlink()
        return f"插件 {plugin_key} 移除成功!"
