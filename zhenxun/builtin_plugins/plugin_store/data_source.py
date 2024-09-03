import shutil
import subprocess
from pathlib import Path

import ujson as json
from aiocache import cached

from zhenxun.services.log import logger
from zhenxun.utils.http_utils import AsyncHttpx
from zhenxun.models.plugin_info import PluginInfo
from zhenxun.utils.image_utils import RowStyle, BuildImage, ImageTemplate
from zhenxun.builtin_plugins.auto_update.config import REQ_TXT_FILE_STRING
from zhenxun.builtin_plugins.plugin_store.models import (
    FileInfo,
    FileType,
    RepoInfo,
    JsdPackageInfo,
    StorePluginInfo,
)

from .config import (
    BASE_PATH,
    EXTRA_GITHUB_URL,
    DEFAULT_GITHUB_URL,
    JSD_PACKAGE_API_FORMAT,
)


def row_style(column: str, text: str) -> RowStyle:
    """被动技能文本风格

    参数:
        column: 表头
        text: 文本内容

    返回:
        RowStyle: RowStyle
    """
    style = RowStyle()
    if column == "-" and text == "已安装":
        style.font_color = "#67C23A"
    return style


def full_files_path(
    jsd_package_info: JsdPackageInfo, module_path: str, is_dir: bool = True
) -> list[FileInfo]:
    """
    获取文件路径

    参数:
        jsd_package_info: JsdPackageInfo
        module_path: 模块路径
        is_dir: 是否为目录

    返回:
        list[FileInfo]: 文件路径
    """
    paths: list[str] = module_path.split(".")
    cur_files: list[FileInfo] = jsd_package_info.files
    for path in paths:
        for cur_file in cur_files:
            if (
                cur_file.type == FileType.DIR
                and cur_file.name == path
                and cur_file.files
                and (is_dir or path != paths[-1])
            ):
                cur_files = cur_file.files
                break
            if not is_dir and path == paths[-1] and cur_file.name.split(".")[0] == path:
                return cur_files
        else:
            raise ValueError(f"模块路径 {module_path} 不存在")
    return cur_files


def recurrence_files(
    files: list[FileInfo], dir_path: str, is_dir: bool = True
) -> list[str]:
    """
    递归获取文件路径

    参数:
        files: 文件列表
        dir_path: 目录路径
        is_dir: 是否为目录

    返回:
        list[str]: 文件路径
    """
    paths = []
    for file in files:
        if is_dir and file.type == FileType.DIR and file.files:
            paths.extend(
                recurrence_files(file.files, f"{dir_path}/{file.name}", is_dir)
            )
        elif file.type == FileType.FILE:
            if dir_path.endswith(file.name):
                paths.append(dir_path)
            elif is_dir:
                paths.append(f"{dir_path}/{file.name}")
    return paths


def install_requirement(plugin_path: Path):
    requirement_files = ["requirement.txt", "requirements.txt"]
    requirement_paths = [plugin_path / file for file in requirement_files]

    existing_requirements = next(
        (path for path in requirement_paths if path.exists()), None
    )

    if not existing_requirements:
        logger.debug(
            f"No requirement.txt found for plugin: {plugin_path.name}", "插件管理"
        )
        return

    try:
        result = subprocess.run(
            ["pip", "install", "-r", str(existing_requirements)],
            check=True,
            capture_output=True,
            text=True,
        )
        logger.debug(
            "Successfully installed dependencies for"
            f" plugin: {plugin_path.name}. Output:\n{result.stdout}",
            "插件管理",
        )
    except subprocess.CalledProcessError:
        logger.error(
            f"Failed to install dependencies for plugin: {plugin_path.name}. "
            " Error:\n{e.stderr}"
        )


class ShopManage:
    @classmethod
    @cached(60)
    async def __get_data(cls) -> dict[str, StorePluginInfo]:
        """获取插件信息数据

        异常:
            ValueError: 访问请求失败

        返回:
            dict: 插件信息数据
        """
        default_github_url = await RepoInfo.parse_github_url(
            DEFAULT_GITHUB_URL
        ).get_download_url_with_path("plugins.json")
        extra_github_url = await RepoInfo.parse_github_url(
            EXTRA_GITHUB_URL
        ).get_download_url_with_path("plugins.json")
        res = await AsyncHttpx.get(default_github_url)
        res2 = await AsyncHttpx.get(extra_github_url)

        # 检查请求结果
        if res.status_code != 200 or res2.status_code != 200:
            raise ValueError(f"下载错误, code: {res.status_code}, {res2.status_code}")

        # 解析并合并返回的 JSON 数据
        data1 = json.loads(res.text)
        data2 = json.loads(res2.text)
        return {
            name: StorePluginInfo(**detail)
            for name, detail in {**data1, **data2}.items()
        }

    @classmethod
    def version_check(cls, plugin_info: StorePluginInfo, suc_plugin: dict[str, str]):
        """版本检查

        参数:
            plugin_info: StorePluginInfo
            suc_plugin: dict[str, str]

        返回:
            str: 版本号
        """
        module = plugin_info.module
        if suc_plugin.get(module) and not cls.check_version_is_new(
            plugin_info, suc_plugin
        ):
            return f"{suc_plugin[module]} (有更新->{plugin_info.version})"
        return plugin_info.version

    @classmethod
    def check_version_is_new(
        cls, plugin_info: StorePluginInfo, suc_plugin: dict[str, str]
    ):
        """检查版本是否有更新

        参数:
            plugin_info: StorePluginInfo
            suc_plugin: dict[str, str]

        返回:
            bool: 是否有更新
        """
        module = plugin_info.module
        return suc_plugin.get(module) and plugin_info.version == suc_plugin[module]

    @classmethod
    async def get_loaded_plugins(cls, *args) -> list[tuple[str, str]]:
        """获取已加载的插件

        返回:
            list[str]: 已加载的插件
        """
        return await PluginInfo.filter(load_status=True).values_list(*args)

    @classmethod
    async def get_plugins_info(cls) -> BuildImage | str:
        """插件列表

        返回:
            BuildImage | str: 返回消息
        """
        data: dict[str, StorePluginInfo] = await cls.__get_data()
        column_name = ["-", "ID", "名称", "简介", "作者", "版本", "类型"]
        plugin_list = await cls.get_loaded_plugins("module", "version")
        suc_plugin = {p[0]: (p[1] or "0.1") for p in plugin_list}
        data_list = [
            [
                "已安装" if plugin_info[1].module in suc_plugin else "",
                id,
                plugin_info[0],
                plugin_info[1].description,
                plugin_info[1].author,
                cls.version_check(plugin_info[1], suc_plugin),
                plugin_info[1].plugin_type_name,
            ]
            for id, plugin_info in enumerate(data.items())
        ]
        return await ImageTemplate.table_page(
            "插件列表",
            "通过添加/移除插件 ID 来管理插件",
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
        data: dict[str, StorePluginInfo] = await cls.__get_data()
        if plugin_id < 0 or plugin_id >= len(data):
            return "插件ID不存在..."
        plugin_key = list(data.keys())[plugin_id]
        plugin_list = await cls.get_loaded_plugins("module")
        plugin_info = data[plugin_key]
        if plugin_info.module in [p[0] for p in plugin_list]:
            return f"插件 {plugin_key} 已安装，无需重复安装"
        is_external = True
        if plugin_info.github_url is None:
            plugin_info.github_url = DEFAULT_GITHUB_URL
            is_external = False
        logger.info(f"正在安装插件 {plugin_key}...")
        await cls.install_plugin_with_repo(
            plugin_info.github_url,
            plugin_info.module_path,
            plugin_info.is_dir,
            is_external,
        )
        return f"插件 {plugin_key} 安装成功! 重启后生效"

    @classmethod
    async def get_repo_package_info_of_jsd(cls, repo_info: RepoInfo) -> JsdPackageInfo:
        """获取插件包信息

        参数:
            repo_info: 仓库信息

        返回:
            JsdPackageInfo: 插件包信息
        """
        jsd_package_url: str = JSD_PACKAGE_API_FORMAT.format(
            owner=repo_info.owner, repo=repo_info.repo, branch=repo_info.branch
        )
        res = await AsyncHttpx.get(url=jsd_package_url)
        if res.status_code != 200:
            raise ValueError(f"下载错误, code: {res.status_code}")
        return JsdPackageInfo(**res.json())

    @classmethod
    async def install_plugin_with_repo(
        cls, github_url: str, module_path: str, is_dir: bool, is_external: bool = False
    ):
        repo_info = RepoInfo.parse_github_url(github_url)
        logger.debug(f"成功获取仓库信息: {repo_info}", "插件管理")
        jsd_package_info: JsdPackageInfo = await cls.get_repo_package_info_of_jsd(
            repo_info=repo_info
        )
        files = full_files_path(jsd_package_info, module_path, is_dir)
        files = recurrence_files(
            files,
            module_path.replace(".", "/") + ("" if is_dir else ".py"),
            is_dir,
        )
        logger.debug(f"获取插件文件列表: {files}", "插件管理")
        download_urls = [
            await repo_info.get_download_url_with_path(file) for file in files
        ]
        base_path = BASE_PATH / "plugins" if is_external else BASE_PATH
        download_paths: list[Path | str] = [base_path / file for file in files]
        logger.debug(f"插件下载路径: {download_paths}", "插件管理")
        result = await AsyncHttpx.gather_download_file(download_urls, download_paths)
        for _id, success in enumerate(result):
            if not success:
                break
        else:
            # 安装依赖
            plugin_path = base_path / "/".join(module_path.split("."))
            req_files = recurrence_files(
                jsd_package_info.files, REQ_TXT_FILE_STRING, False
            )
            req_files.extend(
                recurrence_files(jsd_package_info.files, "requirement.txt", False)
            )
            logger.debug(f"获取插件依赖文件列表: {req_files}", "插件管理")
            req_download_urls = [
                await repo_info.get_download_url_with_path(file) for file in req_files
            ]
            req_paths: list[Path | str] = [plugin_path / file for file in req_files]
            logger.debug(f"插件依赖文件下载路径: {req_paths}", "插件管理")
            if req_files:
                result = await AsyncHttpx.gather_download_file(
                    req_download_urls, req_paths
                )
                for _id, success in enumerate(result):
                    if not success:
                        break
                else:
                    logger.debug(f"插件依赖文件列表: {req_paths}", "插件管理")
                    install_requirement(plugin_path)
                raise Exception("插件依赖文件下载失败")
            return True
        raise Exception("插件下载失败")

    @classmethod
    async def remove_plugin(cls, plugin_id: int) -> str:
        """移除插件

        参数:
            plugin_id: 插件id

        返回:
            str: 返回消息
        """
        data = await cls.__get_data()
        if plugin_id < 0 or plugin_id >= len(data):
            return "插件ID不存在..."
        plugin_key = list(data.keys())[plugin_id]
        plugin_info = data[plugin_key]
        path = BASE_PATH
        if plugin_info.github_url:
            path = BASE_PATH / "plugins"
        for p in plugin_info.module_path.split("."):
            path = path / p
        if not plugin_info.is_dir:
            path = Path(f"{path}.py")
        if not path.exists():
            return f"插件 {plugin_key} 不存在..."
        logger.debug(f"尝试移除插件 {plugin_key} 文件: {path}", "插件管理")
        if plugin_info.is_dir:
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
        data = await cls.__get_data()
        plugin_list = await cls.get_loaded_plugins("module", "version")
        suc_plugin = {p[0]: (p[1] or "Unknown") for p in plugin_list}
        filtered_data = [
            (id, plugin_info)
            for id, plugin_info in enumerate(data.items())
            if plugin_name_or_author.lower() in plugin_info[0].lower()
            or plugin_name_or_author.lower() in plugin_info[1].author.lower()
        ]

        data_list = [
            [
                "已安装" if plugin_info[1].module in suc_plugin else "",
                id,
                plugin_info[0],
                plugin_info[1].description,
                plugin_info[1].author,
                cls.version_check(plugin_info[1], suc_plugin),
                plugin_info[1].plugin_type_name,
            ]
            for id, plugin_info in filtered_data
        ]
        if not data_list:
            return "未找到相关插件..."
        column_name = ["-", "ID", "名称", "简介", "作者", "版本", "类型"]
        return await ImageTemplate.table_page(
            "插件列表",
            "通过添加/移除插件 ID 来管理插件",
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
        data = await cls.__get_data()
        if plugin_id < 0 or plugin_id >= len(data):
            return "插件ID不存在..."
        plugin_key = list(data.keys())[plugin_id]
        logger.info(f"尝试更新插件 {plugin_key}", "插件管理")
        plugin_info = data[plugin_key]
        plugin_list = await cls.get_loaded_plugins("module", "version")
        suc_plugin = {p[0]: (p[1] or "Unknown") for p in plugin_list}
        if plugin_info.module not in [p[0] for p in plugin_list]:
            return f"插件 {plugin_key} 未安装，无法更新"
        logger.debug(f"当前插件列表: {suc_plugin}", "插件管理")
        if cls.check_version_is_new(plugin_info, suc_plugin):
            return f"插件 {plugin_key} 已是最新版本"
        is_external = True
        if plugin_info.github_url is None:
            plugin_info.github_url = DEFAULT_GITHUB_URL
            is_external = False
        await cls.install_plugin_with_repo(
            plugin_info.github_url,
            plugin_info.module_path,
            plugin_info.is_dir,
            is_external,
        )
        return f"插件 {plugin_key} 更新成功! 重启后生效"
