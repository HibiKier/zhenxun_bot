from datetime import datetime, timezone, timedelta

from nonebot.adapters import Bot

# from nonebot.adapters.kaiheila import Bot as KaiheilaBot
from nonebot.adapters.onebot.v11 import Bot as v11Bot
from nonebot.adapters.onebot.v12 import Bot as v12Bot

from zhenxun.services.log import logger
from zhenxun.configs.config import Config
from zhenxun.models.level_user import LevelUser
from zhenxun.models.group_member_info import GroupInfoUser

# from nonebot.adapters.discord import Bot as DiscordBot
# from nonebot.adapters.dodo import Bot as DodoBot


class MemberUpdateManage:

    @classmethod
    async def update(cls, bot: Bot, group_id: str):
        if not group_id:
            return logger.warning(
                f"bot: {bot.self_id}，group_id为空，无法更新群成员信息..."
            )
        if isinstance(bot, v11Bot):
            await cls.v11(bot, group_id)
        elif isinstance(bot, v12Bot):
            await cls.v12(bot, group_id)
        # elif isinstance(bot, KaiheilaBot):
        #     await cls.kaiheila(bot, group_id)
        # elif isinstance(bot, DodoBot):
        #     await cls.dodo(bot, group_id)
        # elif isinstance(bot, DiscordBot):
        #     await cls.discord(bot, group_id)

    # @classmethod
    # async def discord(cls, bot: DiscordBot, group_id: str):
    #     # TODO: discord更新群组成员信息
    #     pass

    # @classmethod
    # async def dodo(cls, bot: DodoBot, group_id: str):
    #     page_size = 100
    #     result_size = 100
    #     max_id = 0
    #     exist_member_list = []
    #     group_member_list: list[MemberInfo] = []
    #     while result_size == page_size:
    #         group_member_data = await bot.get_member_list(
    #             island_source_id=group_id, page_size=page_size
    #         )
    #         result_size = len(group_member_data.list)
    #         group_member_list += group_member_data.list
    #         max_id = group_member_data.max_id
    #     if group_member_list:
    #         for user in group_member_list:
    #             exist_member_list.append(user.dodo_source_id)
    #             await GroupInfoUser.update_or_create(
    #                 user_id=user.dodo_source_id,
    #                 group_id=group_id,
    #                 defaults={
    #                     "user_name": user.nick_name or user.personal_nick_name,
    #                     "user_join_time": user.join_time,
    #                     "platform": "dodo",
    #                 },
    #             )
    #     if delete_member_list := list(
    #         set(exist_member_list).difference(
    #             set(await GroupInfoUser.get_group_member_id_list(group_id))
    #         )
    #     ):
    #         await GroupInfoUser.filter(
    #             user_id__in=delete_member_list, group_id=group_id
    #         ).delete()
    #         logger.info(
    #             f"删除已退群用户",
    #             "更新群组成员信息",
    #             group_id=group_id,
    #             platform="dodo",
    #         )

    # @classmethod
    # async def kaiheila(cls, bot: KaiheilaBot, group_id: str):
    #     # TODO: kaiheila 更新群组成员信息
    #     pass

    @classmethod
    async def v11(cls, bot: v11Bot, group_id: str):
        exist_member_list = []
        default_auth = Config.get_config("admin_bot_manage", "ADMIN_DEFAULT_AUTH")
        group_member_list = await bot.get_group_member_list(group_id=int(group_id))
        db_user = await GroupInfoUser.filter(group_id=group_id).all()
        db_user_uid = [u.user_id for u in db_user]
        uid2name = {u.user_id: u.user_name for u in db_user}
        create_list = []
        update_list = []
        delete_list = []
        for user_info in group_member_list:
            user_id = str(user_info["user_id"])
            nickname = user_info["card"] or user_info["nickname"]
            role = user_info["role"]
            if (
                default_auth
                and role in ["owner", "admin"]
                and not await LevelUser.is_group_flag(user_id, group_id)
            ):
                if role == "owner":
                    await LevelUser.set_level(user_id, group_id, default_auth + 1)
                else:
                    await LevelUser.set_level(user_id, group_id, default_auth)
            if user_id in bot.config.superusers:
                await LevelUser.set_level(user_id, group_id, 9)
            join_time = datetime.fromtimestamp(
                user_info["join_time"], timezone(timedelta(hours=8))
            )
            if cnt := db_user_uid.count(user_id):
                users = [u for u in db_user if u.user_id == user_id]
                if cnt > 1:
                    for u in users[1:]:
                        delete_list.append(u.id)
                if nickname != uid2name.get(user_id):
                    user = users[0]
                    user.user_name = nickname
                    update_list.append(user)
            else:
                create_list.append(
                    GroupInfoUser(
                        user_id=user_id,
                        group_id=group_id,
                        user_name=nickname,
                        user_join_time=join_time,
                        platform="qq",
                    )
                )
            exist_member_list.append(user_id)
        if create_list:
            await GroupInfoUser.bulk_create(create_list, 30)
            logger.debug(
                f"创建用户数据 {len(create_list)} 条",
                "更新群组成员信息",
                target=group_id,
            )
        if update_list:
            await GroupInfoUser.bulk_update(update_list, ["user_name"], 30)
            logger.debug(
                f"更新户数据 {len(update_list)} 条", "更新群组成员信息", target=group_id
            )
        if delete_list:
            await GroupInfoUser.filter(id__in=delete_list).delete()
            logger.debug(f"删除重复数据 Ids: {delete_list}", "更新群组成员信息")

        if delete_member_list := [
            uid for uid in db_user_uid if uid not in exist_member_list
        ]:
            await GroupInfoUser.filter(
                user_id__in=delete_member_list, group_id=group_id
            ).delete()
            logger.info(
                f"删除已退群用户 {len(delete_member_list)} 条",
                "更新群组成员信息",
                group_id=group_id,
                platform="qq",
            )

    @classmethod
    async def v12(cls, bot: v12Bot, group_id: str):
        # TODO: v12更新群组成员信息
        pass
        # exist_member_list = []
        # default_auth = Config.get_config("admin_bot_manage", "ADMIN_DEFAULT_AUTH")
        # group_member_list: list[GetGroupMemberInfoResp] =
        # await bot.get_group_member_list(
        #     group_id=group_id
        # )
        # for user_info in group_member_list:
        #     user_id = user_info.user_id
        #     nickname = user_info.user_displayname or user_info.user_name
        #     role = user_info["role"]
        #     if default_auth:
        #         if role in ["owner", "admin"] and not LevelUser.is_group_flag(
        #             str(user_id), group_id
        #         ):
        #             await LevelUser.set_level(user_id, group_id, default_auth)
        #     if str(user_id) in bot.config.superusers:
        #         await LevelUser.set_level(str(user_id), group_id, 9)
        #     join_time = datetime.strptime(
        #         time.strftime("%Y-%m-%d %H:%M:%S",
        # time.localtime(user_info["join_time"])),
        #         "%Y-%m-%d %H:%M:%S",
        #     )
        #     await GroupInfoUser.update_or_create(
        #         user_id=str(user_id),
        #         group_id=group_id,
        #         defaults={
        #             "user_name": nickname,
        #             "user_join_time": join_time.replace(
        #                 tzinfo=timezone(timedelta(hours=8))
        #             ),
        #         },
        #     )
        #     exist_member_list.append(str(user_id))
        #     logger.debug("更新成功", "更新群组成员信息",
        # session=user_id, group_id=group_id)
        # if delete_member_list := list(
        #     set(exist_member_list).difference(
        #         set(await GroupInfoUser.get_group_member_id_list(group_id))
        #     )
        # ):
        #     await GroupInfoUser.filter(
        #         user_id__in=delete_member_list, group_id=group_id
        #     ).delete()
        #     logger.info(f"删除已退群用户", "更新群组成员信息", group_id=group_id)
