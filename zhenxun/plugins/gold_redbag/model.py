from tortoise import fields

from zhenxun.services.db_context import Model


class RedbagUser(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_id = fields.CharField(255)
    """用户id"""
    group_id = fields.CharField(255)
    """群聊id"""
    send_redbag_count = fields.IntField(default=0)
    """发送红包次数"""
    get_redbag_count = fields.IntField(default=0)
    """开启红包次数"""
    spend_gold = fields.IntField(default=0)
    """发送红包花费金额"""
    get_gold = fields.IntField(default=0)
    """开启红包获取金额"""

    class Meta:
        table = "redbag_users"
        table_description = "红包统计数据表"
        unique_together = ("user_id", "group_id")

    @classmethod
    async def add_redbag_data(
        cls, user_id: str, group_id: str, i_type: str, money: int
    ):
        """添加收发红包数据

        参数:
            user_id: 用户id
            group_id: 群号
            i_type: 收或发
            money: 金钱数量
        """

        user, _ = await cls.get_or_create(user_id=user_id, group_id=group_id)
        if i_type == "get":
            user.get_redbag_count = user.get_redbag_count + 1
            user.get_gold = user.get_gold + money
        else:
            user.send_redbag_count = user.send_redbag_count + 1
            user.spend_gold = user.spend_gold + money
        await user.save(
            update_fields=[
                "get_redbag_count",
                "get_gold",
                "send_redbag_count",
                "spend_gold",
            ]
        )

    @classmethod
    async def _run_script(cls):
        return [
            "ALTER TABLE redbag_users RENAME COLUMN user_qq TO user_id;",  # 将user_qq改为user_id
            "ALTER TABLE redbag_users ALTER COLUMN user_id TYPE character varying(255);",
            "ALTER TABLE redbag_users ALTER COLUMN group_id TYPE character varying(255);",
        ]
