import re
import shutil
import subprocess
from pathlib import Path

import ujson as json

from zhenxun.models.plugin_info import PluginInfo
from zhenxun.services.log import logger
from zhenxun.utils.http_utils import AsyncHttpx
from zhenxun.utils.image_utils import BuildImage, ImageTemplate, RowStyle

from .config import BASE_PATH, CONFIG_URL, CONFIG_INDEX_URL, CONFIG_INDEX_CDN_URL, DOWNLOAD_URL


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
        url: str, data_list: list[tuple[str, str]], ignore_list: list[str] = [], api_url: str = None
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
            _url = api_url + path if api_url else DOWNLOAD_URL.format(path)
            if _url not in ignore_list:
                ignore_list.append(_url)
                await recurrence_get_url(_url, data_list, ignore_list, api_url)


async def download_file(url: str, _is: bool = False, api_url: str = None):
    """下载文件

    参数:
        url: 插件详情url
        _is: 是否为第三方插件
        url_start : 第三方插件url

    异常:
        ValueError: 下载失败
    """
    data_list = []
    await recurrence_get_url(url, data_list, api_url=api_url)
    for download_url, path in data_list:
        if download_url and "." in path:
            logger.debug(f"下载文件: {path}", "插件管理")
            base_path = "zhenxun/plugins/" if _is else "zhenxun/"
            file = Path(f"{base_path}{path}")
            file.parent.mkdir(parents=True, exist_ok=True)
            print(download_url)
            r = await AsyncHttpx.get(download_url)
            if r.status_code != 200:
                raise ValueError(f"文件下载错误, code: {r.status_code}")
            content = r.text.replace("\r\n", "\n")  # 统一换行符为 UNIX 风格
            with open(file, "w", encoding="utf8") as f:
                logger.debug(f"写入文件: {file}", "插件管理")
                f.write(content)


def install_requirement(plugin_path: Path):
    requirement_files = ["requirement.txt", "requirements.txt"]
    requirement_paths = [plugin_path / file for file in requirement_files]

    existing_requirements = next((path for path in requirement_paths if path.exists()), None)

    if not existing_requirements:
        logger.debug(f"No requirement.txt found for plugin: {plugin_path.name}", "插件管理")
        return

    try:
        result = subprocess.run(
            ["pip", "install", "-r", str(existing_requirements)],
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
        res2 = await AsyncHttpx.get(CONFIG_INDEX_URL)

        if res2.status_code != 200:
            logger.info("访问第三方插件信息文件失败，改为进行cdn访问")
            res2 = await AsyncHttpx.get(CONFIG_INDEX_CDN_URL)

        # 检查请求结果
        if res.status_code != 200 or res2.status_code != 200:
            raise ValueError(f"下载错误, code: {res.status_code}, {res2.status_code}")

        # 解析并合并返回的 JSON 数据
        data1 = json.loads(res.text)
        data2 = json.loads(res2.text)
        return {**data1, **data2}

    @classmethod
    def version_check(cls, plugin_info: dict, suc_plugin: dict[str, str]):
        module = plugin_info["module"]
        if module in suc_plugin:
            if plugin_info["version"] != suc_plugin[module]:
                return f"{suc_plugin[module]} (有更新->{plugin_info['version']})"
        return plugin_info["version"]

    @classmethod
    def get_url_path(cls, module_path: str, is_dir: bool) -> str:
        url_path = None
        path = BASE_PATH
        module_path_split = module_path.split(".")
        if len(module_path_split) == 2:
            """单个文件或文件夹"""
            if is_dir:
                url_path = "/".join(module_path_split)
            else:
                url_path = "/".join(module_path_split) + ".py"
        else:
            """嵌套文件或文件夹"""
            for p in module_path_split[:-1]:
                path = path / p
            path.mkdir(parents=True, exist_ok=True)
            if is_dir:
                url_path = f"{'/'.join(module_path_split)}"
            else:
                url_path = f"{'/'.join(module_path_split)}.py"
        return url_path

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
        plugin_list = await PluginInfo.filter(load_status=True).values_list(
            "module", "version"
        )
        suc_plugin = {p[0]: p[1] for p in plugin_list if p[1]}
        data_list = [
            [
                "已安装" if plugin_info[1]["module"] in suc_plugin else "",
                id,
                plugin_info[0],
                plugin_info[1]["description"],
                plugin_info[1]["author"],
                cls.version_check(plugin_info[1], suc_plugin),
                plugin_info[1]["plugin_type"],
            ]
            for id, plugin_info in enumerate(data.items())
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
        """添加插件

        参数:
            plugin_id: 插件id

        返回:
            str: 返回消息
        """
        data: dict = await cls.__get_data()
        if plugin_id < 0 or plugin_id >= len(data):
            return "插件ID不存在..."
        plugin_key = list(data.keys())[plugin_id]
        plugin_info = data[plugin_key]
        module_path_split = plugin_info["module_path"].split(".")
        url_path = cls.get_url_path(plugin_info["module_path"], plugin_info["is_dir"])
        if not url_path and plugin_info["module_path"]:
            return "插件下载地址构建失败..."
        logger.debug(f"尝试下载插件 URL: {url_path}", "插件管理")
        github_url = plugin_info.get("github_url")
        if github_url:
            github_path = re.search(r"github\.com/([^/]+/[^/]+)", github_url).group(1)
            api_url = f"https://api.github.com/repos/{github_path}/contents/"
            download_url = f"{api_url}{url_path}?ref=main"
        else:
            download_url = DOWNLOAD_URL.format(url_path)
            api_url = None

        await download_file(download_url, bool(github_url), api_url)

        # 安装依赖
        plugin_path = BASE_PATH / "/".join(module_path_split)
        if url_path and github_url:
            plugin_path = BASE_PATH / "plugins" / "/".join(module_path_split)
            res = await AsyncHttpx.get(api_url)
            if res.status_code != 200:
                return f"访问错误, code: {res.status_code}"
            json_data = res.json()
            requirement_file = next(
                (v for v in json_data if v["name"] in ["requirements.txt", "requirement.txt"]), None
            )
            if requirement_file:
                r = await AsyncHttpx.get(requirement_file.get("download_url"))
                if r.status_code != 200:
                    raise ValueError(f"文件下载错误, code: {r.status_code}")
                requirement_path = plugin_path / requirement_file["name"]
                with open(requirement_path, "w", encoding="utf8") as f:
                    logger.debug(f"写入文件: {requirement_path}", "插件管理")
                    f.write(r.text)

        install_requirement(plugin_path)

        return f"插件 {plugin_key} 安装成功! 重启后生效"

    @classmethod
    async def remove_plugin(cls, plugin_id: int) -> str:
        """移除插件

        参数:
            plugin_id: 插件id

        返回:
            str: 返回消息
        """
        data: dict = await cls.__get_data()
        if plugin_id < 0 or plugin_id >= len(data):
            return "插件ID不存在..."
        plugin_key = list(data.keys())[plugin_id]
        plugin_info = data[plugin_key]
        path = BASE_PATH
        github_url = plugin_info.get("github_url")
        if github_url:
            path = BASE_PATH / 'plugins'
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
        return f"插件 {plugin_key} 移除成功! 重启后生效"

    @classmethod
    async def search_plugin(cls, plugin_name_or_author: str) -> BuildImage | str:
        """搜索插件

        参数:
            plugin_name_or_author: 插件名称或作者

        返回:
            BuildImage | str: 返回消息
        """
        data: dict = await cls.__get_data()
        column_name = ["-", "ID", "名称", "简介", "作者", "版本", "类型"]
        for k in data.copy():
            if data[k]["plugin_type"]:
                data[k]["plugin_type"] = cls.type2name[data[k]["plugin_type"]]
        plugin_list = await PluginInfo.filter(load_status=True).values_list(
            "module", "version"
        )
        suc_plugin = {p[0]: p[1] for p in plugin_list if p[1]}
        filtered_data = [
            (id, plugin_info)
            for id, plugin_info in enumerate(data.items())
            if plugin_name_or_author.lower() in plugin_info[0].lower()
               or plugin_name_or_author.lower() in plugin_info[1]["author"].lower()
        ]

        data_list = [
            [
                "已安装" if plugin_info[1]["module"] in suc_plugin else "",
                id,
                plugin_info[0],
                plugin_info[1]["description"],
                plugin_info[1]["author"],
                cls.version_check(plugin_info[1], suc_plugin),
                plugin_info[1]["plugin_type"],
            ]
            for id, plugin_info in filtered_data
        ]
        if not data_list:
            return "未找到相关插件..."
        return await ImageTemplate.table_page(
            "插件列表",
            f"通过安装/卸载插件 ID 来管理插件",
            column_name,
            data_list,
            text_style=row_style,
        )

    @classmethod
    async def update_plugin(cls, plugin_id: int) -> str:
        """更新插件

        参数:
            plugin_id: 插件id

        返回:
            str: 返回消息
        """
        data: dict = await cls.__get_data()
        if plugin_id < 0 or plugin_id >= len(data):
            return "插件ID不存在..."
        plugin_key = list(data.keys())[plugin_id]
        plugin_info = data[plugin_key]
        module_path_split = plugin_info["module_path"].split(".")
        url_path = cls.get_url_path(plugin_info["module_path"], plugin_info["is_dir"])
        if not url_path and plugin_info["module_path"]:
            return "插件下载地址构建失败..."
        logger.debug(f"尝试下载插件 URL: {url_path}", "插件管理")
        github_url = plugin_info.get("github_url")
        if github_url:
            github_path = re.search(r"github\.com/([^/]+/[^/]+)", github_url).group(1)
            api_url = f"https://api.github.com/repos/{github_path}/contents/"
            download_url = f"{api_url}{url_path}?ref=main"
        else:
            download_url = DOWNLOAD_URL.format(url_path)
            api_url = None

        await download_file(download_url, bool(github_url), api_url)

        # 安装依赖
        plugin_path = BASE_PATH / "/".join(module_path_split)
        if url_path and github_url:
            plugin_path = BASE_PATH / "plugins" / "/".join(module_path_split)
            res = await AsyncHttpx.get(api_url)
            if res.status_code != 200:
                return f"访问错误, code: {res.status_code}"
            json_data = res.json()
            requirement_file = next(
                (v for v in json_data if v["name"] in ["requirements.txt", "requirement.txt"]), None
            )
            if requirement_file:
                r = await AsyncHttpx.get(requirement_file.get("download_url"))
                if r.status_code != 200:
                    raise ValueError(f"文件下载错误, code: {r.status_code}")
                requirement_path = plugin_path / requirement_file["name"]
                with open(requirement_path, "w", encoding="utf8") as f:
                    logger.debug(f"写入文件: {requirement_path}", "插件管理")
                    f.write(r.text)

        install_requirement(plugin_path)

        return f"插件 {plugin_key} 更新成功! 重启后生效"
