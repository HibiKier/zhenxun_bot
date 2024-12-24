from pydantic import BaseModel


class MenuItem(BaseModel):
    module: str
    """模块名称"""
    name: str
    """菜单名称"""
    router: str
    """路由"""
    icon: str
    """图标"""
    default: bool = False
    """默认选中"""


class MenuData(BaseModel):
    bot_type: str = "zhenxun"
    """bot类型"""
    menus: list[MenuItem]
    """菜单列表"""
