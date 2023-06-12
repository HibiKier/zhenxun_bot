from datetime import datetime, timedelta
from typing import Any, Tuple

import pytz
from nonebot import on_regex
from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.params import RegexGroup

from models.chat_history import ChatHistory
from models.group_member_info import GroupInfoUser
from utils.image_utils import BuildImage, text2image
from utils.message_builder import image
from utils.utils import is_number

__zx_plugin_name__ = "消息统计"
__plugin_usage__ = """
usage：
    发言记录统计
    regex：(周|月|日)?消息排行(des|DES)?(n=[0-9]{1,2})?
    指令：
        消息统计?(des)?(n=?)
        周消息统计?(des)?(n=?)
        月消息统计?(des)?(n=?)
        日消息统计?(des)?(n=?)
    示例：
        消息统计
        消息统计des
        消息统计DESn=15
        消息统计n=15
""".strip()
__plugin_des__ = "发言消息排行"
__plugin_cmd__ = ["消息统计", "周消息统计", "月消息统计", "日消息统计"]
__plugin_type__ = ("数据统计", 1)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "cmd": ["消息统计"],
}


msg_handler = on_regex(
    r"^(周|月|日)?消息统计(des|DES)?(n=[0-9]{1,2})?$", priority=5, block=True
)


@msg_handler.handle()
async def _(event: GroupMessageEvent, reg_group: Tuple[Any, ...] = RegexGroup()):
    gid = event.group_id
    date_scope = None
    date, order, num = reg_group
    num = num.split("=")[-1] if num else 10
    if num and is_number(num) and 10 < int(num) < 50:
        num = int(num)
    time_now = datetime.now()
    zero_today = time_now - timedelta(
        hours=time_now.hour, minutes=time_now.minute, seconds=time_now.second
    )
    if date in ["日"]:
        date_scope = (zero_today, time_now)
    elif date in ["周"]:
        date_scope = (time_now - timedelta(days=7), time_now)
    elif date in ["月"]:
        date_scope = (time_now - timedelta(days=30), time_now)
    if rank_data := await ChatHistory.get_group_msg_rank(
        gid, num, order or "DESC", date_scope
    ):
        name = "昵称：\n\n"
        num_str = "发言次数：\n\n"
        idx = 1
        for uid, num in rank_data:
            if user := await GroupInfoUser.filter(user_id=uid, group_id=gid).first():
                user_name = user.user_name
            else:
                user_name = uid
            name += f"\t{idx}.{user_name} \n\n"
            num_str += f"\t{num}\n\n"
            idx += 1
        name_img = await text2image(name.strip(), padding=10, color="#f9f6f2")
        num_img = await text2image(num_str.strip(), padding=10, color="#f9f6f2")
        if not date_scope:
            if date_scope := await ChatHistory.get_group_first_msg_datetime(gid):
                date_scope = date_scope.astimezone(
                    pytz.timezone("Asia/Shanghai")
                ).replace(microsecond=0)
            else:
                date_scope = time_now.replace(microsecond=0)
            date_str = f"日期：{date_scope} - 至今"
        else:
            date_str = f"日期：{date_scope[0].replace(microsecond=0)} - {date_scope[1].replace(microsecond=0)}"
        date_w = BuildImage(0, 0, font_size=15).getsize(date_str)[0]
        img_w = date_w if date_w > name_img.w + num_img.w else name_img.w + num_img.w
        A = BuildImage(
            img_w + 15,
            num_img.h + 30,
            color="#f9f6f2",
            font="CJGaoDeGuo.otf",
            font_size=15,
        )
        await A.atext((10, 10), date_str)
        await A.apaste(name_img, (0, 30))
        await A.apaste(num_img, (name_img.w, 30))
        await msg_handler.send(image(b64=A.pic2bs4()))


# @test.handle()
# async def _(event: MessageEvent):
#     print(await ChatHistory.get_user_msg(event.user_id, "private"))
#     print(await ChatHistory.get_user_msg_count(event.user_id, "private"))
#     print(await ChatHistory.get_user_msg(event.user_id, "group"))
#     print(await ChatHistory.get_user_msg_count(event.user_id, "group"))
#     print(await ChatHistory.get_group_msg(event.group_id))
#     print(await ChatHistory.get_group_msg_count(event.group_id))
