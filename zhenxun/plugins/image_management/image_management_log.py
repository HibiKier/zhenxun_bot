from tortoise import fields

from zhenxun.services.db_context import Model

from ._config import ImageHandleType


class ImageManagementLog(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_id = fields.CharField(255, description="用户id")
    """用户id"""
    path = fields.TextField(description="图片路径")
    """图片路径"""
    move = fields.TextField(null=True, description="移动路径")
    """移动路径"""
    handle_type = fields.CharEnumField(ImageHandleType, description="操作类型")
    """操作类型"""
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    """创建时间"""
    platform = fields.CharField(255, null=True, description="平台")
    """平台"""

    class Meta:
        table = "image_management_log"
        table_description = "画廊操作记录"
