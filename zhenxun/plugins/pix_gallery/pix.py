import random

from nonebot.adapters import Bot
from nonebot.plugin import PluginMetadata
from nonebot_plugin_alconna import (
    Alconna,
    Args,
    Arparma,
    Match,
    Option,
    on_alconna,
    store_true,
)
from nonebot_plugin_session import EventSession

from zhenxun.configs.config import Config
from zhenxun.configs.utils import BaseBlock, PluginExtraData, RegisterConfig
from zhenxun.services.log import logger
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.platform import PlatformUtils
from zhenxun.utils.withdraw_manage import WithdrawManager

from ._data_source import get_image
from ._model.omega_pixiv_illusts import OmegaPixivIllusts
from ._model.pixiv import Pixiv

__plugin_meta__ = PluginMetadata(
    name="PIX",
    description="这里是PIX图库！",
    usage="""
    指令：
        pix ?*[tags]: 通过 tag 获取相似图片，不含tag时随机抽取
        pid [uid]: 通过uid获取图片
        pix pid[pid]: 查看图库中指定pid图片
        示例：pix 萝莉 白丝
        示例：pix 萝莉 白丝 10  （10为数量）
        示例：pix #02      （当tag只有1个tag且为数字时，使用#标记，否则将被判定为数量）
        示例：pix 34582394     （查询指定uid图片）
        示例：pix pid:12323423     （查询指定pid图片）
    """.strip(),
    extra=PluginExtraData(
        author="HibiKier",
        version="0.1",
        superuser_help="""
        指令：
            pix -s ?*[tags]: 通过tag获取色图，不含tag时随机
            pix -r ?*[tags]: 通过tag获取r18图，不含tag时随机
        """,
        menu_type="来点好康的",
        limits=[BaseBlock(result="您有PIX图片正在处理，请稍等...")],
        configs=[
            RegisterConfig(
                key="MAX_ONCE_NUM2FORWARD",
                value=None,
                help="单次发送的图片数量达到指定值时转发为合并消息",
                default_value=None,
                type=int,
            ),
            RegisterConfig(
                key="ALLOW_GROUP_SETU",
                value=False,
                help="允许非超级用户使用-s参数",
                default_value=False,
                type=bool,
            ),
            RegisterConfig(
                key="ALLOW_GROUP_R18",
                value=False,
                help="允许非超级用户使用-r参数",
                default_value=False,
                type=bool,
            ),
        ],
    ).dict(),
)

# pix = on_command("pix", aliases={"PIX", "Pix"}, priority=5, block=True)

_matcher = on_alconna(
    Alconna(
        "pix",
        Args["tags?", str] / "\n",
        Option("-s", action=store_true, help_text="色图"),
        Option("-r", action=store_true, help_text="r18"),
    ),
    priority=5,
    block=True,
)

PIX_RATIO = None
OMEGA_RATIO = None


@_matcher.handle()
async def _(bot: Bot, session: EventSession, arparma: Arparma, tags: Match[str]):
    global PIX_RATIO, OMEGA_RATIO
    gid = session.id3 or session.id2
    if not session.id1:
        await MessageUtils.build_message("用户id为空...").finish()
    if PIX_RATIO is None:
        pix_omega_pixiv_ratio = Config.get_config("pix", "PIX_OMEGA_PIXIV_RATIO")
        PIX_RATIO = pix_omega_pixiv_ratio[0] / (
            pix_omega_pixiv_ratio[0] + pix_omega_pixiv_ratio[1]
        )
        OMEGA_RATIO = 1 - PIX_RATIO
    num = 1
    # keyword = arg.extract_plain_text().strip()
    keyword = ""
    spt = tags.result.split() if tags.available else []
    if arparma.find("s"):
        nsfw_tag = 1
    elif arparma.find("r"):
        nsfw_tag = 2
    else:
        nsfw_tag = 0
    if session.id1 not in bot.config.superusers:
        if (nsfw_tag == 1 and not Config.get_config("pix", "ALLOW_GROUP_SETU")) or (
            nsfw_tag == 2 and not Config.get_config("pix", "ALLOW_GROUP_R18")
        ):
            await MessageUtils.build_message(
                "你不能看这些噢，这些都是是留给管理员看的..."
            ).finish()
    if (n := len(spt)) == 1:
        if str(spt[0]).isdigit() and int(spt[0]) < 100:
            num = int(spt[0])
            keyword = ""
        elif spt[0].startswith("#"):
            keyword = spt[0][1:]
    elif n > 1:
        if str(spt[-1]).isdigit():
            num = int(spt[-1])
            if num > 10:
                if session.id1 not in bot.config.superusers or (
                    session.id1 in bot.config.superusers and num > 30
                ):
                    num = random.randint(1, 10)
                    await MessageUtils.build_message(
                        f"太贪心了，就给你发 {num}张 好了"
                    ).send()
            spt = spt[:-1]
            keyword = " ".join(spt)
    pix_num = int(num * PIX_RATIO) + 15 if PIX_RATIO != 0 else 0
    omega_num = num - pix_num + 15
    if str(keyword).isdigit():
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
        if not str(pid).isdigit():
            await MessageUtils.build_message("PID必须是数字...").finish(reply_to=True)
        all_image = await Pixiv.query_images(
            pid=int(pid), r18=1 if nsfw_tag == 2 else 0
        )
        if not all_image:
            all_image = await OmegaPixivIllusts.query_images(
                pid=int(pid), nsfw_tag=nsfw_tag
            )
        num = len(all_image)
    else:
        tmp = await Pixiv.query_images(
            spt, r18=1 if nsfw_tag == 2 else 0, num=pix_num
        ) + await OmegaPixivIllusts.query_images(spt, nsfw_tag=nsfw_tag, num=omega_num)
        tmp_ = []
        all_image = []
        for x in tmp:
            if x.pid not in tmp_:
                all_image.append(x)
                tmp_.append(x.pid)
    if not all_image:
        await MessageUtils.build_message(
            f"未在图库中找到与 {keyword} 相关Tag/UID/PID的图片..."
        ).finish(reply_to=True)
    msg_list = []
    for _ in range(num):
        img_url = None
        author = None
        if not all_image:
            await MessageUtils.build_message("坏了...发完了，没图了...").finish()
        img = random.choice(all_image)
        all_image.remove(img)  # type: ignore
        if isinstance(img, OmegaPixivIllusts):
            img_url = img.url
            author = img.uname
        elif isinstance(img, Pixiv):
            img_url = img.img_url
            author = img.author
        pid = img.pid
        title = img.title
        uid = img.uid
        if img_url:
            _img = await get_image(img_url, session.id1)
            if _img:
                if Config.get_config("pix", "SHOW_INFO"):
                    msg_list.append(
                        MessageUtils.build_message(
                            [
                                f"title：{title}\n"
                                f"author：{author}\n"
                                f"PID：{pid}\nUID：{uid}\n",
                                _img,
                            ]
                        )
                    )
                else:
                    msg_list.append(_img)
                logger.info(
                    f" 查看PIX图库PID: {pid}", arparma.header_result, session=session
                )
            else:
                msg_list.append(MessageUtils.build_message("这张图似乎下载失败了"))
                logger.info(
                    f" 查看PIX图库PID: {pid}，下载图片出错",
                    arparma.header_result,
                    session=session,
                )
    if (
        Config.get_config("pix", "MAX_ONCE_NUM2FORWARD")
        and num >= Config.get_config("pix", "MAX_ONCE_NUM2FORWARD")
        and gid
    ):
        for msg in msg_list:
            receipt = await msg.send()
            if receipt:
                message_id = receipt.msg_ids[0]["message_id"]
                await WithdrawManager.withdraw_message(
                    bot,
                    str(message_id),
                    Config.get_config("pix", "WITHDRAW_PIX_MESSAGE"),
                    session,
                )
    else:
        for msg in msg_list:
            receipt = await msg.send()
            if receipt:
                message_id = receipt.msg_ids[0]["message_id"]
                await WithdrawManager.withdraw_message(
                    bot,
                    message_id,
                    Config.get_config("pix", "WITHDRAW_PIX_MESSAGE"),
                    session,
                )
