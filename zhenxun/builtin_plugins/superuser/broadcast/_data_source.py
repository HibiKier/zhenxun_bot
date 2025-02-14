from nonebot.adapters import Bot
import nonebot_plugin_alconna as alc

# from nonebot.adapters.discord import Bot as DiscordBot
# from nonebot.adapters.dodo import Bot as DodoBot
# from nonebot.adapters.kaiheila import Bot as KaiheilaBot
# from nonebot.adapters.onebot.v11 import Bot as v11Bot
# from nonebot.adapters.onebot.v12 import Bot as v12Bot
from nonebot_plugin_alconna import Image, UniMsg
from nonebot_plugin_session import EventSession

from zhenxun.services.log import logger
from zhenxun.utils.common_utils import CommonUtils
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.platform import PlatformUtils


class BroadcastManage:
    @classmethod
    async def send(
        cls, bot: Bot, message: UniMsg, session: EventSession
    ) -> tuple[int, int]:
        """发送广播消息

        参数:
            bot: Bot
            message: 消息内容
            session: Session

        返回:
            tuple[int, int]: 发送成功的群组数量, 发送失败的群组数量
        """
        message_list = []
        for msg in message:
            if isinstance(msg, alc.Image) and msg.url:
                message_list.append(Image(url=msg.url))
            elif isinstance(msg, alc.Text):
                message_list.append(msg.text)
        group_list, _ = await PlatformUtils.get_group_list(bot)
        if group_list:
            error_count = 0
            for group in group_list:
                try:
                    if not await CommonUtils.task_is_block(
                        bot,
                        "broadcast",  # group.channel_id
                        group.group_id,
                    ):
                        target = PlatformUtils.get_target(
                            group_id=group.group_id, channel_id=group.channel_id
                        )
                        if target:
                            await MessageUtils.build_message(message_list).send(
                                target, bot
                            )
                            logger.debug(
                                "发送成功",
                                "广播",
                                session=session,
                                target=f"{group.group_id}:{group.channel_id}",
                            )
                        else:
                            logger.warning("target为空", "广播", session=session)
                except Exception as e:
                    error_count += 1
                    logger.error(
                        "发送失败",
                        "广播",
                        session=session,
                        target=f"{group.group_id}:{group.channel_id}",
                        e=e,
                    )
            return len(group_list) - error_count, error_count
        return 0, 0
