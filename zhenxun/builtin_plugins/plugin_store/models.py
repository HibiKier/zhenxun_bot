from pydantic import BaseModel

from zhenxun.utils.enum import PluginType

type2name: dict[str, str] = {
    "NORMAL": "普通插件",
    "ADMIN": "管理员插件",
    "SUPERUSER": "超级用户插件",
    "ADMIN_SUPERUSER": "管理员/超级用户插件",
    "DEPENDANT": "依赖插件",
    "HIDDEN": "其他插件",
}


class StorePluginInfo(BaseModel):
    """插件信息"""

    module: str
    module_path: str
    description: str
    usage: str
    author: str
    version: str
    plugin_type: PluginType
    is_dir: bool
    github_url: str | None

    @property
    def plugin_type_name(self):
        return type2name[self.plugin_type.value]
