from utils.utils import is_number
from configs.config import Config
from ._model.omega_pixiv_illusts import OmegaPixivIllusts
from utils.message_builder import image, custom_forward_msg
from utils.manager import withdraw_message_manager
from services.log import logger
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, Message
from nonebot.params import CommandArg
from ._data_source import get_image
from ._model.pixiv import Pixiv
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
__plugin_configs__ = {
    "MAX_ONCE_NUM2FORWARD": {
        "value": None,
        "help": "单次发送的图片数量达到指定值时转发为合并消息",
        "default_value": None,
    }
}


pix = on_command("pix", aliases={"PIX", "Pix"}, priority=5, block=True)


PIX_RATIO = None
OMEGA_RATIO = None


@pix.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    global PIX_RATIO, OMEGA_RATIO
    if PIX_RATIO is None:
        pix_omega_pixiv_ratio = Config.get_config("pix", "PIX_OMEGA_PIXIV_RATIO")
        PIX_RATIO = pix_omega_pixiv_ratio[0] / (
            pix_omega_pixiv_ratio[0] + pix_omega_pixiv_ratio[1]
        )
        OMEGA_RATIO = 1 - PIX_RATIO
    num = 1
    keyword = arg.extract_plain_text().strip()
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
    if n := len(x) == 1 and is_number(x[0]):
        num = int(x[-1])
        keyword = ""
    elif n > 1:
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
    if is_number(keyword):
        if num == 1:
            pix_num = 15
            omega_num = 15
        all_image = await Pixiv.query_images(
            uid=int(keyword), num=pix_num, r18=1 if nsfw_tag == 2 else 0
        ) + await OmegaPixivIllusts.query_images(
            uid=int(keyword), num=omega_num, nsfw_tag=nsfw_tag
        )
    elif keyword.lower().startswith("pid"):
        pid = keyword.replace("pid", "").replace(":", "").replace("：", "")
        if not is_number(pid):
            await pix.finish("PID必须是数字...", at_sender=True)
        all_image = await Pixiv.query_images(
            pid=int(pid), r18=1 if nsfw_tag == 2 else 0
        )
        if not all_image:
            all_image = await OmegaPixivIllusts.query_images(
                pid=int(pid), nsfw_tag=nsfw_tag
            )
    else:
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
    msg_list = []
    for _ in range(num):
        img_url = None
        author = None
        # if not all_image:
        #     await pix.finish("坏了...发完了，没图了...")
        img = random.choice(all_image)
        all_image.remove(img)
        if isinstance(img, OmegaPixivIllusts):
            img_url = img.url
            author = img.uname
        elif isinstance(img, Pixiv):
            img_url = img.img_url
            author = img.author
        pid = img.pid
        title = img.title
        uid = img.uid
        _img = await get_image(img_url, event.user_id)
        if _img:
            if Config.get_config("pix", "SHOW_INFO"):
                msg_list.append(
                    Message(
                        f"title：{title}\n"
                        f"author：{author}\n"
                        f"PID：{pid}\nUID：{uid}\n"
                        f"{image(_img)}"
                    )
                )
            else:
                msg_list.append(image(_img))
            logger.info(
                f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
                f" 查看PIX图库PID: {pid}"
            )
        else:
            msg_list.append("这张图似乎下载失败了")
            logger.info(
                f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
                f" 查看PIX图库PID: {pid}，下载图片出错"
            )
    if (
        Config.get_config("pix", "MAX_ONCE_NUM2FORWARD")
        and num >= Config.get_config("pix", "MAX_ONCE_NUM2FORWARD")
        and isinstance(event, GroupMessageEvent)
    ):
        msg_id = await bot.send_group_forward_msg(
            group_id=event.group_id, messages=custom_forward_msg(msg_list, bot.self_id)
        )
        withdraw_message_manager.withdraw_message(
            event, msg_id, Config.get_config("pix", "WITHDRAW_PIX_MESSAGE")
        )
    else:
        for msg in msg_list:
            msg_id = await pix.send(msg)
            withdraw_message_manager.withdraw_message(
                event, msg_id, Config.get_config("pix", "WITHDRAW_PIX_MESSAGE")
            )
