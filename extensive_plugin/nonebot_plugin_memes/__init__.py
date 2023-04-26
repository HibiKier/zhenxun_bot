import hashlib
import random
import traceback
from io import BytesIO
from itertools import chain
from typing import Any, Dict, List, NoReturn, Type, Union

from meme_generator.exception import (
    ArgMismatch,
    ArgParserExit,
    MemeGeneratorException,
    TextOrNameNotEnough,
    TextOverLength,
)
from meme_generator.meme import Meme, MemeParamsType
from meme_generator.utils import TextProperties, render_meme_list
from nonebot import on_command, on_message, require
from nonebot.adapters.onebot.v11 import Bot as V11Bot
from nonebot.adapters.onebot.v11 import GroupMessageEvent as V11GMEvent
from nonebot.adapters.onebot.v11 import Message as V11Msg
from nonebot.adapters.onebot.v11 import MessageEvent as V11MEvent
from nonebot.adapters.onebot.v11 import MessageSegment as V11MsgSeg
from nonebot.adapters.onebot.v11.permission import (
    GROUP_ADMIN,
    GROUP_OWNER,
    PRIVATE_FRIEND,
)
from nonebot.adapters.onebot.v12 import Bot as V12Bot
from nonebot.adapters.onebot.v12 import ChannelMessageEvent as V12CMEvent
from nonebot.adapters.onebot.v12 import GroupMessageEvent as V12GMEvent
from nonebot.adapters.onebot.v12 import Message as V12Msg
from nonebot.adapters.onebot.v12 import MessageEvent as V12MEvent
from nonebot.adapters.onebot.v12 import MessageSegment as V12MsgSeg
from nonebot.adapters.onebot.v12.permission import PRIVATE
from nonebot.exception import AdapterException
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Depends
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_Handler, T_State
from nonebot.utils import run_sync
from pypinyin import Style, pinyin

require("nonebot_plugin_localstore")

from nonebot_plugin_localstore import get_cache_dir

from .config import memes_config
from .data_source import ImageSource, User, UserInfo
from .depends import (
    IMAGE_SOURCES_KEY,
    TEXTS_KEY,
    USERS_KEY,
    split_msg_v11,
    split_msg_v12,
)
from .exception import NetworkError, PlatformUnsupportError
from .manager import ActionResult, MemeMode, meme_manager
from .rule import command_rule, regex_rule
from .utils import meme_info
# ======================== zhenxun import ===============================
from io import BytesIO
from typing import Union
from nonebot.params import Depends
from nonebot.matcher import Matcher
from nonebot.typing import T_Handler
from nonebot import on_command, require
from nonebot.adapters.onebot.v11 import MessageSegment
from configs.path_config import IMAGE_PATH


__zx_plugin_name__ = "表情包制作"
__plugin_usage__ = """
usage：
    触发方式：指令 + @user/qq/自己/图片
    发送“表情包制作”查看表情包列表
    指令： 
        摸 @任何人
        摸 qq号
        摸 自己
        摸 [图片]
""".strip()
__plugin_des__ = "制作各种沙雕表情包"
__plugin_type__ = ("工具",)
__plugin_cmd__ = ["表情包制作", "头像表情包", "文字表情包"]
__plugin_version__ = 0.45
__plugin_author__ = "MeetWq"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    'cmd': __plugin_cmd__
}
__plugin_resources__ = {
    "images": IMAGE_PATH / "petpet", }
# ======================== zhenxun import ===============================

# help_cmd = on_command("头像表情包", aliases={"头像相关表情包", "头像相关表情制作"}, block=True, priority=5)

# __plugin_meta__ = PluginMetadata(
#     name="表情包制作",
#     description="制作各种沙雕表情包",
#     usage="发送“表情包制作”查看表情包列表",
#     extra={
#         "unique_name": "memes",
#         "author": "meetwq <meetwq@gmail.com>",
#         "version": "0.4.5",
#     },
# )

memes_cache_dir = get_cache_dir("nonebot_plugin_memes")


# PERM_EDIT = GROUP_ADMIN | GROUP_OWNER | PRIVATE_FRIEND | PRIVATE | SUPERUSER
# PERM_GLOBAL = SUPERUSER

help_cmd = on_command("表情包制作", aliases={"头像表情包", "文字表情包"}, block=True, priority=5)
info_cmd = on_command("表情详情", aliases={"表情帮助", "表情示例"}, block=True, priority=5)
block_cmd = on_command("禁用表情", block=True, priority=9)
unblock_cmd = on_command("启用表情", block=True, priority=9)
block_cmd_gl = on_command("全局禁用表情", block=True, priority=9)
unblock_cmd_gl = on_command("全局启用表情", block=True, priority=9)


def get_user_id():
    def dependency(
        bot: Union[V11Bot, V12Bot], event: Union[V11MEvent, V12MEvent]
    ) -> str:
        if isinstance(event, V11MEvent):
            cid = f"{bot.self_id}_{event.message_type}_"
        else:
            cid = f"{bot.self_id}_{event.detail_type}_"

        if isinstance(event, V11GMEvent) or isinstance(event, V12GMEvent):
            cid += str(event.group_id)
        elif isinstance(event, V12CMEvent):
            cid += f"{event.guild_id}_{event.channel_id}"
        else:
            cid += str(event.user_id)
        return cid

    return Depends(dependency)


@help_cmd.handle()
async def _(bot: Union[V11Bot, V12Bot], matcher: Matcher, user_id: str = get_user_id()):
    memes = sorted(
        meme_manager.memes,
        key=lambda meme: "".join(
            chain.from_iterable(pinyin(meme.keywords[0], style=Style.TONE3))
        ),
    )
    meme_list = [
        (
            meme,
            TextProperties(
                fill="black" if meme_manager.check(user_id, meme.key) else "lightgrey"
            ),
        )
        for meme in memes
    ]

    # cache rendered meme list
    meme_list_hashable = [
        ({"key": meme.key, "keywords": meme.keywords}, prop) for meme, prop in meme_list
    ]
    meme_list_hash = hashlib.md5(str(meme_list_hashable).encode("utf8")).hexdigest()
    meme_list_cache_file = memes_cache_dir / f"{meme_list_hash}.jpg"
    if not meme_list_cache_file.exists():
        img = await run_sync(render_meme_list)(meme_list)
        with open(meme_list_cache_file, "wb") as f:
            f.write(img.getvalue())
    else:
        img = BytesIO(meme_list_cache_file.read_bytes())

    msg = "触发方式：“关键词 + 图片/文字”\n发送 “表情详情 + 关键词” 查看表情参数和预览\n目前支持的表情列表："

    if isinstance(bot, V11Bot):
        await matcher.finish(msg + V11MsgSeg.image(img))
    else:
        resp = await bot.upload_file(type="data", name="memes", data=img.getvalue())
        file_id = resp["file_id"]
        await matcher.finish(msg + V12MsgSeg.image(file_id))


@info_cmd.handle()
async def _(
    bot: Union[V11Bot, V12Bot],
    matcher: Matcher,
    msg: Union[V11Msg, V12Msg] = CommandArg(),
):
    meme_name = msg.extract_plain_text().strip()
    if not meme_name:
        matcher.block = False
        await matcher.finish()

    if not (meme := meme_manager.find(meme_name)):
        await matcher.finish(f"表情 {meme_name} 不存在！")

    info = meme_info(meme)
    info += "表情预览：\n"
    img = await meme.generate_preview()

    if isinstance(bot, V11Bot):
        await matcher.finish(info + V11MsgSeg.image(img))
    else:
        resp = await bot.upload_file(type="data", name="memes", data=img.getvalue())
        file_id = resp["file_id"]
        await matcher.finish(info + V12MsgSeg.image(file_id))


@block_cmd.handle()
async def _(
    matcher: Matcher,
    msg: Union[V11Msg, V12Msg] = CommandArg(),
    user_id: str = get_user_id(),
):
    meme_names = msg.extract_plain_text().strip().split()
    if not meme_names:
        matcher.block = False
        await matcher.finish()
    results = meme_manager.block(user_id, meme_names)
    messages = []
    for name, result in results.items():
        if result == ActionResult.SUCCESS:
            message = f"表情 {name} 禁用成功"
        elif result == ActionResult.NOTFOUND:
            message = f"表情 {name} 不存在！"
        else:
            message = f"表情 {name} 禁用失败"
        messages.append(message)
    await matcher.finish("\n".join(messages))


@unblock_cmd.handle()
async def _(
    matcher: Matcher,
    msg: Union[V11Msg, V12Msg] = CommandArg(),
    user_id: str = get_user_id(),
):
    meme_names = msg.extract_plain_text().strip().split()
    if not meme_names:
        matcher.block = False
        await matcher.finish()
    results = meme_manager.unblock(user_id, meme_names)
    messages = []
    for name, result in results.items():
        if result == ActionResult.SUCCESS:
            message = f"表情 {name} 启用成功"
        elif result == ActionResult.NOTFOUND:
            message = f"表情 {name} 不存在！"
        else:
            message = f"表情 {name} 启用失败"
        messages.append(message)
    await matcher.finish("\n".join(messages))


@block_cmd_gl.handle()
async def _(matcher: Matcher, msg: Union[V11Msg, V12Msg] = CommandArg()):
    meme_names = msg.extract_plain_text().strip().split()
    if not meme_names:
        matcher.block = False
        await matcher.finish()
    results = meme_manager.change_mode(MemeMode.WHITE, meme_names)
    messages = []
    for name, result in results.items():
        if result == ActionResult.SUCCESS:
            message = f"表情 {name} 已设为白名单模式"
        elif result == ActionResult.NOTFOUND:
            message = f"表情 {name} 不存在！"
        else:
            message = f"表情 {name} 设置失败"
        messages.append(message)
    await matcher.finish("\n".join(messages))


@unblock_cmd_gl.handle()
async def _(matcher: Matcher, msg: Union[V11Msg, V12Msg] = CommandArg()):
    meme_names = msg.extract_plain_text().strip().split()
    if not meme_names:
        matcher.block = False
        await matcher.finish()
    results = meme_manager.change_mode(MemeMode.BLACK, meme_names)
    messages = []
    for name, result in results.items():
        if result == ActionResult.SUCCESS:
            message = f"表情 {name} 已设为黑名单模式"
        elif result == ActionResult.NOTFOUND:
            message = f"表情 {name} 不存在！"
        else:
            message = f"表情 {name} 设置失败"
        messages.append(message)
    await matcher.finish("\n".join(messages))


async def process(
    bot: Union[V11Bot, V12Bot],
    matcher: Matcher,
    meme: Meme,
    image_sources: List[ImageSource],
    texts: List[str],
    users: List[User],
    args: Dict[str, Any] = {},
):
    images: List[bytes] = []
    user_infos: List[UserInfo] = []

    try:
        for image_source in image_sources:
            images.append(await image_source.get_image())
    except PlatformUnsupportError as e:
        await matcher.finish(f"当前平台 “{e.platform}” 暂不支持获取头像，请使用图片输入")
    except (NetworkError, AdapterException):
        logger.warning(traceback.format_exc())
        await matcher.finish("图片下载出错，请稍后再试")

    try:
        for user in users:
            user_infos.append(await user.get_info())
        args["user_infos"] = user_infos
    except (NetworkError, AdapterException):
        logger.warning("用户信息获取失败\n" + traceback.format_exc())

    try:
        result = await meme(images=images, texts=texts, args=args)
    except TextOverLength as e:
        await matcher.finish(f"文字 “{e.text}” 长度过长")
    except ArgMismatch:
        await matcher.finish("参数解析错误")
    except TextOrNameNotEnough:
        await matcher.finish("文字或名字数量不足")
    except MemeGeneratorException:
        logger.warning(traceback.format_exc())
        await matcher.finish("出错了，请稍后再试")

    if isinstance(bot, V11Bot):
        await matcher.finish(V11MsgSeg.image(result))
    else:
        resp = await bot.upload_file(type="data", name="memes", data=result.getvalue())
        file_id = resp["file_id"]
        await matcher.finish(V12MsgSeg.image(file_id))


def handler(meme: Meme) -> T_Handler:
    async def handle(
        bot: Union[V11Bot, V12Bot],
        state: T_State,
        matcher: Matcher,
        user_id: str = get_user_id(),
    ):
        if not meme_manager.check(user_id, meme.key):
            return

        raw_texts: List[str] = state[TEXTS_KEY]
        users: List[User] = state[USERS_KEY]
        image_sources: List[ImageSource] = state[IMAGE_SOURCES_KEY]

        texts: List[str] = []
        args: Dict[str, Any] = {}

        async def finish(msg: str) -> NoReturn:
            logger.info(msg)
            if memes_config.memes_prompt_params_error:
                matcher.stop_propagation()
                await matcher.finish(msg)
            await matcher.finish()

        if meme.params_type.args_type:
            try:
                parse_result = meme.parse_args(raw_texts)
            except ArgParserExit:
                await finish(f"参数解析错误")
            texts = parse_result["texts"]
            parse_result.pop("texts")
            args = parse_result
        else:
            texts = raw_texts

        if not (
            meme.params_type.min_images
            <= len(image_sources)
            <= meme.params_type.max_images
        ):
            await finish(
                f"输入图片数量不符，图片数量应为 {meme.params_type.min_images}"
                + (
                    f" ~ {meme.params_type.max_images}"
                    if meme.params_type.max_images > meme.params_type.min_images
                    else ""
                )
            )
        if not (meme.params_type.min_texts <= len(texts) <= meme.params_type.max_texts):
            await finish(
                f"输入文字数量不符，文字数量应为 {meme.params_type.min_texts}"
                + (
                    f" ~ {meme.params_type.max_texts}"
                    if meme.params_type.max_texts > meme.params_type.min_texts
                    else ""
                )
            )

        matcher.stop_propagation()
        await process(bot, matcher, meme, image_sources, texts, users, args)

    return handle


def create_matchers():
    for meme in meme_manager.memes:
        matchers: List[Type[Matcher]] = []
        if meme.keywords:
            matchers.append(
                on_message(command_rule(meme.keywords), block=False, priority=12)
            )
        if meme.patterns:
            matchers.append(
                on_message(regex_rule(meme.patterns), block=False, priority=13)
            )

        for matcher in matchers:
            matcher.append_handler(handler(meme), parameterless=[split_msg_v11(meme)])
            matcher.append_handler(handler(meme), parameterless=[split_msg_v12(meme)])

    async def random_handler(
        bot: Union[V11Bot, V12Bot], state: T_State, matcher: Matcher
    ):
        texts: List[str] = state[TEXTS_KEY]
        users: List[User] = state[USERS_KEY]
        image_sources: List[ImageSource] = state[IMAGE_SOURCES_KEY]

        random_meme = random.choice(
            [
                meme
                for meme in meme_manager.memes
                if (
                    (
                        meme.params_type.min_images
                        <= len(image_sources)
                        <= meme.params_type.max_images
                    )
                    and (
                        meme.params_type.min_texts
                        <= len(texts)
                        <= meme.params_type.max_texts
                    )
                )
            ]
        )
        await process(bot, matcher, random_meme, image_sources, texts, users)

    random_matcher = on_message(command_rule(["随机表情"]), block=False, priority=12)
    fake_meme = Meme("_fake", _, MemeParamsType())
    random_matcher.append_handler(
        random_handler, parameterless=[split_msg_v11(fake_meme)]
    )
    random_matcher.append_handler(
        random_handler, parameterless=[split_msg_v12(fake_meme)]
    )


create_matchers()
