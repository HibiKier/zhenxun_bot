from tortoise import fields

from zhenxun.services.db_context import Model
from zhenxun.utils.enum import BlockType, PluginType

from .plugin_limit import PluginLimit


class PluginInfo(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    module = fields.CharField(255, description="模块名")
    """模块名"""
    module_path = fields.CharField(255, description="模块路径", unique=True)
    """模块路径"""
    name = fields.CharField(255, description="插件名称")
    """插件名称"""
    status = fields.BooleanField(default=True, description="全局开关状态")
    """全局开关状态"""
    block_type: BlockType | None = fields.CharEnumField(
        BlockType, default=None, null=True, description="禁用类型"
    )
    """禁用类型"""
    load_status = fields.BooleanField(default=True, description="加载状态")
    """加载状态"""
    author = fields.CharField(255, null=True, description="作者")
    """作者"""
    version = fields.CharField(max_length=255, null=True, description="版本")
    """版本"""
    level = fields.IntField(default=5, description="所需群权限")
    """所需群权限"""
    default_status = fields.BooleanField(default=True, description="进群默认开关状态")
    """进群默认开关状态"""
    limit_superuser = fields.BooleanField(default=False, description="是否限制超级用户")
    """是否限制超级用户"""
    menu_type = fields.CharField(max_length=255, default="功能", description="菜单类型")
    """菜单类型"""
    plugin_type = fields.CharEnumField(PluginType, null=True, description="插件类型")
    """插件类型"""
    cost_gold = fields.IntField(default=0, description="调用插件所需金币")
    """调用插件所需金币"""
    plugin_limit = fields.ReverseRelation["PluginLimit"]
    """插件限制"""
    admin_level = fields.IntField(default=0, null=True, description="调用所需权限等级")
    """调用所需权限等级"""
    is_delete = fields.BooleanField(default=False, description="是否删除")
    """是否删除"""

    class Meta:
        table = "plugin_info"
        table_description = "插件基本信息"
