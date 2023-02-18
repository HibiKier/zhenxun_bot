from nonebot import on_command
from nonebot.adapters.onebot.v11 import ActionFailed, GroupMessageEvent, Message
from nonebot.adapters.onebot.v11.permission import GROUP
from nonebot.params import CommandArg

from models.bag_user import BagUser
from utils.data_utils import init_rank
from utils.image_utils import text2image
from utils.message_builder import image
from utils.utils import is_number

__zx_plugin_name__ = "商店 - 我的金币"
__plugin_usage__ = """
usage：
    我的金币
    指令：
        我的金币
""".strip()
__plugin_des__ = "商店 - 我的金币"
__plugin_cmd__ = ["我的金币"]
__plugin_type__ = ("商店",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["商店", "我的金币"],
}


my_gold = on_command("我的金币", priority=5, block=True, permission=GROUP)

gold_rank = on_command("金币排行", priority=5, block=True, permission=GROUP)


@my_gold.handle()
async def _(event: GroupMessageEvent):
    msg = await BagUser.get_user_total_gold(event.user_id, event.group_id)
    try:
        await my_gold.send(msg)
    except ActionFailed:
        await my_gold.send(
            image(b64=(await text2image(msg, color="#f9f6f2", padding=10)).pic2bs4())
        )


@gold_rank.handle()
async def _(event: GroupMessageEvent, arg: Message = CommandArg()):
    num = arg.extract_plain_text().strip()
    if is_number(num) and 51 > int(num) > 10:
        num = int(num)
    else:
        num = 10
    all_users = await BagUser.filter(group_id=event.group_id)
    all_user_id = [user.user_qq for user in all_users]
    all_user_data = [user.gold for user in all_users]
    rank_image = await init_rank(
        "金币排行", all_user_id, all_user_data, event.group_id, num
    )
    if rank_image:
        await gold_rank.finish(image(b64=rank_image.pic2bs4()))
