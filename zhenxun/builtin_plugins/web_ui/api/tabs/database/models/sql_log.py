from tortoise import fields

from zhenxun.services.db_context import Model


class SqlLog(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    ip = fields.CharField(255)
    """ip"""
    sql = fields.CharField(255)
    """sql"""
    result = fields.CharField(255, null=True)
    """结果"""
    is_suc = fields.BooleanField(default=True)
    """是否成功"""
    create_time = fields.DatetimeField(auto_now_add=True)
    """创建时间"""

    class Meta:  # pyright: ignore [reportIncompatibleVariableOverride]
        table = "sql_log"
        table_description = "sql执行日志"

    @classmethod
    async def add(
        cls, ip: str, sql: str, result: str | None = None, is_suc: bool = True
    ):
        """获取用户在群内的等级

        参数:
            ip: ip
            sql: sql
            result: 返回结果
            is_suc: 是否成功
        """
        await cls.create(ip=ip, sql=sql, result=result, is_suc=is_suc)
