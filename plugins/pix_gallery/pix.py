from nonebot.adapters.cqhttp.message import Message
from utils.utils import get_message_text, is_number
from configs.config import PIX_OMEGA_PIXIV_RATIO, WITHDRAW_PIX_TIME
from models.omega_pixiv_illusts import OmegaPixivIllusts
from utils.message_builder import image
from services.log import logger
from nonebot.adapters.cqhttp import (
    Bot,
    MessageEvent,
    GroupMessageEvent,
    PrivateMessageEvent,
)
from utils.manager import withdraw_message_manager
from nonebot.typing import T_State
from .data_source import get_image
from models.pixiv import Pixiv
from nonebot import on_command
import random


__zx_plugin_name__ = "PIX"
__plugin_usage__ = """
usage：
    查看 pix 好康图库
    指令：
        pix ?*[tags]: 通过 tag 获取相似图片，不含tag时随机抽取
        pix pid[pid]: 查看图库中指定pid图片
""".strip()
__plugin_superuser_usage__ = """
usage：
    超级用户额外的 pix 指令
    指令：
        pix -s ?*[tags]: 通过tag获取色图，不含tag时随机
        pix -r ?*[tags]: 通过tag获取r18图，不含tag时随机
""".strip()
__plugin_des__ = "这里是PIX图库！"
__plugin_cmd__ = [
    "pix ?*[tags]",
    "pix pid [pid]",
    "pix -s ?*[tags] [_superuser]",
    "pix -r ?*[tags] [_superuser]",
]
__plugin_type__ = ("来点好康的",)
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["pix", "Pix", "PIX", "pIx"],
}
__plugin_block_limit__ = {"rst": "您有PIX图片正在处理，请稍等..."}


pix = on_command("pix", aliases={"PIX", "Pix"}, priority=5, block=True)


PIX_RATIO = PIX_OMEGA_PIXIV_RATIO[0] / (
    PIX_OMEGA_PIXIV_RATIO[0] + PIX_OMEGA_PIXIV_RATIO[1]
)
OMEGA_RATIO = 1 - PIX_RATIO


@pix.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    num = 1
    keyword = get_message_text(event.json())
    if is_number(keyword):
        all_image = await Pixiv.query_images(uid=int(keyword))
    elif keyword.lower().startswith("pid"):
        pid = keyword.replace("pid", "").replace(":", "")
        if not is_number(pid):
            await pix.finish("PID必须是数字...", at_sender=True)
        isr18 = 0 if isinstance(event, GroupMessageEvent) else 2
        nsfw_tag = 0 if isinstance(event, GroupMessageEvent) else None
        all_image = await Pixiv.query_images(pid=int(pid), r18=isr18)
        if not all_image:
            all_image = await OmegaPixivIllusts.query_images(
                pid=int(pid), nsfw_tag=nsfw_tag
            )
    else:
        x = keyword.split()
        if "-s" in x:
            x.remove("-s")
            nsfw_tag = 1
        elif "-r" in x:
            x.remove("-r")
            nsfw_tag = 2
        else:
            nsfw_tag = 0
        if nsfw_tag != 0 and str(event.user_id) not in bot.config.superusers:
            await pix.finish("你不能看这些噢，这些都是是留给管理员看的...")
        if len(x) > 1:
            if is_number(x[-1]):
                num = int(x[-1])
                if num > 10:
                    if str(event.user_id) not in bot.config.superusers or (
                        str(event.user_id) in bot.config.superusers and num > 30
                    ):
                        num = random.randint(1, 10)
                        await pix.send(f"太贪心了，就给你发 {num}张 好了")
                x = x[:-1]
                keyword = " ".join(x)
        pix_num = int(num * PIX_RATIO) + 15 if PIX_RATIO != 0 else 0
        omega_num = num - pix_num + 15
        tmp = await Pixiv.query_images(
            x, r18=1 if nsfw_tag == 2 else 0, num=pix_num
        ) + await OmegaPixivIllusts.query_images(x, nsfw_tag=nsfw_tag, num=omega_num)
        tmp_ = []
        all_image = []
        for x in tmp:
            if x.pid not in tmp_:
                all_image.append(x)
                tmp_.append(x.pid)
    if not all_image:
        await pix.finish(f"未在图库中找到与 {keyword} 相关Tag/UID/PID的图片...", at_sender=True)
    for _ in range(num):
        img_url = None
        author = None
        if not all_image:
            await pix.finish("坏了...发完了，没图了...")
        img = random.choice(all_image)
        all_image.remove(img)
        if isinstance(img, OmegaPixivIllusts):
            img_url = img.url
            author = img.uname
            print(img.nsfw_tag)
        elif isinstance(img, Pixiv):
            img_url = img.img_url
            author = img.author
        pid = img.pid
        title = img.title
        uid = img.uid
        # tags = img.tags
        _img = await get_image(img_url, event.user_id)
        if _img:
            msg_id = await pix.send(
                Message(
                    f"title：{title}\n"
                    f"author：{author}\n"
                    f"PID：{pid}\nUID：{uid}\n"
                    f"{image(_img, 'temp')}"
                )
            )
            logger.info(
                f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
                f" 查看PIX图库PID: {pid}"
            )
        else:
            msg_id = await pix.send(f"下载图片似乎出了一点问题，PID：{pid}")
            logger.info(
                f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
                f" 查看PIX图库PID: {pid}，下载图片出错"
            )
        withdraw_message(event, msg_id["message_id"])


def withdraw_message(event: MessageEvent, id_: int):
    if WITHDRAW_PIX_TIME[0]:
        if (
            (WITHDRAW_PIX_TIME[1] == 0 and isinstance(event, PrivateMessageEvent))
            or (WITHDRAW_PIX_TIME[1] == 1 and isinstance(event, GroupMessageEvent))
            or WITHDRAW_PIX_TIME[1] == 2
        ):
            withdraw_message_manager.append((id_, WITHDRAW_PIX_TIME[0]))
