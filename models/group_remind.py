from services.db_context import db


class GroupRemind(db.Model):
    __tablename__ = "group_reminds"

    id = db.Column(db.Integer(), primary_key=True)
    group_id = db.Column(db.BigInteger(), nullable=False)
    hy = db.Column(db.Boolean(), default=False)  # 进群欢迎
    kxcz = db.Column(db.Boolean(), default=False)  # 开箱重置
    zwa = db.Column(db.Boolean(), default=False)  # 早晚安
    gb = db.Column(db.Boolean(), default=True)  # 广播
    blpar = db.Column(db.Boolean(), default=True)  # bilibili转发解析
    pa = db.Column(db.Boolean(), default=True)  # 爬
    epic = db.Column(db.Boolean(), default=False)  # epic
    almanac = db.Column(db.Boolean(), default=False)  # 原神黄历

    _idx1 = db.Index("info_group_reminds_idx1", "group_id", unique=True)

    @classmethod
    async def get_status(cls, group_id: int, name: str) -> bool:
        """
        说明：
            获取群通知状态
        参数：
            :param group_id: 群号
            :param name: 目标名称
        """
        group = await cls.query.where((cls.group_id == group_id)).gino.first()
        if not group:
            group = await cls.create(
                group_id=group_id,
            )
        if name == "hy":
            return group.hy
        if name == "kxcz":
            return group.kxcz
        if name == "zwa":
            return group.zwa
        if name == "gb":
            return group.gb
        if name == "blpar":
            return group.blpar
        if name == "epic":
            return group.epic
        if name == "pa":
            return group.pa
        if name == "almanac":
            return group.almanac

    @classmethod
    async def set_status(cls, group_id: int, name: str, status: bool) -> bool:
        """
        说明：
            设置群通知状态
        参数：
            :param group_id: 群号
            :param name: 目标名称
            :param status: 通知状态
        """
        try:
            group = (
                await cls.query.where((cls.group_id == group_id))
                .with_for_update()
                .gino.first()
            )
            if not group:
                group = await cls.create(
                    group_id=group_id,
                )
            if name == "hy":
                await group.update(
                    hy=status,
                ).apply()
            if name == "kxcz":
                await group.update(
                    kxcz=status,
                ).apply()
            if name == "zwa":
                await group.update(
                    zwa=status,
                ).apply()
            if name == "gb":
                await group.update(
                    gb=status,
                ).apply()
            if name == "blpar":
                await group.update(
                    blpar=status,
                ).apply()
            if name == "epic":
                await group.update(
                    epic=status,
                ).apply()
            if name == "pa":
                await group.update(
                    pa=status,
                ).apply()
            if name == "almanac":
                await group.update(
                    almanac=status,
                ).apply()
            return True
        except Exception as e:
            return False
