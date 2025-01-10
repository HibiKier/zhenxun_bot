from nonebot.adapters import Bot
from tortoise import fields

from zhenxun.models.group_console import GroupConsole
from zhenxun.services.db_context import Model
from zhenxun.utils.enum import RequestHandleType, RequestType
from zhenxun.utils.exception import NotFoundError


class FgRequest(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    request_type = fields.CharEnumField(
        RequestType, default=None, description="请求类型"
    )
    """请求类型"""
    platform = fields.CharField(255, description="平台")
    """平台"""
    bot_id = fields.CharField(255, description="Bot Id")
    """botId"""
    flag = fields.CharField(max_length=255, default="", description="flag")
    """flag"""
    user_id = fields.CharField(max_length=255, description="请求用户id")
    """请求用户id"""
    group_id = fields.CharField(max_length=255, null=True, description="邀请入群id")
    """邀请入群id"""
    nickname = fields.CharField(max_length=255, description="请求人名称")
    """对象名称"""
    comment = fields.CharField(max_length=255, null=True, description="验证信息")
    """验证信息"""
    handle_type = fields.CharEnumField(
        RequestHandleType, null=True, description="处理类型"
    )
    """处理类型"""

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "fg_request"
        table_description = "好友群组请求"

    @classmethod
    async def approve(cls, bot: Bot, id: int):
        """同意请求

        参数:
            bot: Bot
            id: 请求id

        异常:
            NotFoundError: 未发现请求
        """
        await cls._handle_request(bot, id, RequestHandleType.APPROVE)

    @classmethod
    async def refused(cls, bot: Bot, id: int):
        """拒绝请求

        参数:
            bot: Bot
            id: 请求id

        异常:
            NotFoundError: 未发现请求
        """
        await cls._handle_request(bot, id, RequestHandleType.REFUSED)

    @classmethod
    async def ignore(cls, id: int):
        """忽略请求

        参数:
            id: 请求id

        异常:
            NotFoundError: 未发现请求
        """
        await cls._handle_request(None, id, RequestHandleType.IGNORE)

    @classmethod
    async def expire(cls, id: int):
        """忽略请求

        参数:
            id: 请求id

        异常:
            NotFoundError: 未发现请求
        """
        await cls._handle_request(None, id, RequestHandleType.EXPIRE)

    @classmethod
    async def _handle_request(
        cls,
        bot: Bot | None,
        id: int,
        handle_type: RequestHandleType,
    ):
        """处理请求

        参数:
            bot: Bot
            id: 请求id
            handle_type: 处理类型

        异常:
            NotFoundError: 未发现请求
        """
        req = await cls.get_or_none(id=id)
        if not req:
            raise NotFoundError
        req.handle_type = handle_type
        await req.save(update_fields=["handle_type"])
        if bot and handle_type not in [
            RequestHandleType.IGNORE,
            RequestHandleType.EXPIRE,
        ]:
            if req.request_type == RequestType.FRIEND:
                await bot.set_friend_add_request(
                    flag=req.flag, approve=handle_type == RequestHandleType.APPROVE
                )
            else:
                await GroupConsole.update_or_create(
                    group_id=req.group_id, defaults={"group_flag": 1}
                )
                await bot.set_group_add_request(
                    flag=req.flag,
                    sub_type="invite",
                    approve=handle_type == RequestHandleType.APPROVE,
                )
