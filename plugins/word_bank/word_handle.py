import re
from typing import Any, List, Optional, Tuple

from nonebot import on_command, on_regex
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message,
    MessageEvent,
    PrivateMessageEvent,
    unescape,
)
from nonebot.exception import FinishedException
from nonebot.internal.params import Arg, ArgStr
from nonebot.params import Command, CommandArg, RegexGroup
from nonebot.typing import T_State

from configs.config import Config
from configs.path_config import DATA_PATH
from services.log import logger
from utils.depends import AtList, ImageList
from utils.message_builder import custom_forward_msg
from utils.utils import get_message_at, get_message_img, is_number

from ._config import scope2int, type2int
from ._data_source import delete_word, show_word, update_word
from ._model import WordBank

__zx_plugin_name__ = "词库问答 [Admin]"
__plugin_usage__ = r"""
usage：
    对指定问题的随机回答，对相同问题可以设置多个不同回答
    删除词条后每个词条的id可能会变化，请查看后再删除
    更推荐使用id方式删除
    问题回答支持的CQ：at, face, image
    查看词条命令：群聊时为 群词条+全局词条，私聊时为 私聊词条+全局词条
    添加词条正则：添加词条(模糊|正则|图片)?问\s*?(\S*\s?\S*)\s*?答\s?(\S*)
    正则问可以通过$1类推()捕获的组
    指令：
        添加词条 ?[模糊|正则|图片]问...答...：添加问答词条，可重复添加相同问题的不同回答
        删除词条 [问题/下标] ?[下标]：删除指定词条指定或全部回答
        修改词条 [问题/下标] [新问题]：修改词条问题
        查看词条 ?[问题/下标]：查看全部词条或对应词条回答
        示例：添加词条问图片答嗨嗨嗨
            [图片]...
        示例：添加词条@萝莉 我来啦
        示例：添加词条问谁是萝莉答是我
        示例：添加词条正则问那个(.+)是萝莉答没错$1是萝莉
        示例：删除词条 谁是萝莉
        示例：删除词条 谁是萝莉 0
        示例：删除词条 id:0 1
        示例：修改词条 谁是萝莉 是你
        示例：修改词条 id:0 是你
        示例：查看词条
        示例：查看词条 谁是萝莉
        示例：查看词条 id:0    (群/私聊词条)
        示例：查看词条 gid:0   (全局词条)
""".strip()
__plugin_superuser_usage__ = r"""
usage:
    在私聊中超级用户额外设置
    指令：
        (全局|私聊)?添加词条\s*?(模糊|正则|图片)?问\s*?(\S*\s?\S*)\s*?答\s?(\S*)：添加问答词条，可重复添加相同问题的不同回答
        全局添加词条
        私聊添加词条
        （私聊情况下）删除词条: 删除私聊词条
        （私聊情况下）删除全局词条
        （私聊情况下）修改词条: 修改私聊词条
        （私聊情况下）修改全局词条
        用法与普通用法相同
""".strip()
__plugin_des__ = "自定义词条内容随机回复"
__plugin_cmd__ = [
    "添加词条 ?[模糊/关键字]问...答..",
    "删除词条 [问题/下标] ?[下标]",
    "修改词条 [问题/下标] ?[下标/新回答] [新回答]",
    "查看词条 ?[问题/下标]",
]
__plugin_version__ = 0.3
__plugin_author__ = "HibiKier & yajiwa"
__plugin_settings__ = {
    "admin_level": Config.get_config("word_bank", "WORD_BANK_LEVEL [LEVEL]"),
    "cmd": ["词库问答", "添加词条", "删除词条", "修改词条", "查看词条"],
}

data_dir = DATA_PATH / "word_bank"
data_dir.mkdir(parents=True, exist_ok=True)

add_word = on_regex(
    r"^(全局|私聊)?添加词条\s*?(模糊|正则|图片)?问\s*?(\S*\s?\S*)\s*?答\s?(\S*)", priority=5, block=True
)

delete_word_matcher = on_command("删除词条", aliases={"删除全局词条"}, priority=5, block=True)

update_word_matcher = on_command("修改词条", aliases={"修改全局词条"}, priority=5, block=True)

show_word_matcher = on_command("显示词条", aliases={"查看词条"}, priority=5, block=True)


@add_word.handle()
async def _(
    bot: Bot,
    event: MessageEvent,
    state: T_State,
    reg_group: Tuple[Any, ...] = RegexGroup(),
    img_list: List[str] = ImageList(),
    at_list: List[int] = AtList(),
):
    if (
        isinstance(event, PrivateMessageEvent)
        and str(event.user_id) not in bot.config.superusers
    ):
        await add_word.finish("权限不足捏")
    word_scope, word_type, problem, answer = reg_group
    if not word_scope and isinstance(event, PrivateMessageEvent):
        word_scope = "私聊"
    if (
        word_scope
        and word_scope in ["全局", "私聊"]
        and str(event.user_id) not in bot.config.superusers
    ):
        await add_word.finish("权限不足，无法添加该范围词条")
    if (not problem or not problem.strip()) and word_type != "图片":
        await add_word.finish("词条问题不能为空！")
    if (not answer or not answer.strip()) and not len(img_list) and not len(at_list):
        await add_word.finish("词条回答不能为空！")
    if word_type != "图片":
        state["problem_image"] = "YES"
    answer = event.message
    # 对at问题对额外处理
    if at_list:
        is_first = True
        cur_p = None
        answer = ""
        problem = ""
        for index, seg in enumerate(event.message):
            if seg.type == "text" and "添加词条问" in str(seg) and is_first:
                is_first = False
                seg_ = str(seg).split("添加词条问")[-1]
                cur_p = "problem"
                # 纯文本
                if "答" in seg_:
                    answer_index = seg_.index("答")
                    problem = unescape(seg_[:answer_index]).strip()
                    answer = unescape(seg_[answer_index + 1 :]).strip()
                    cur_p = "answer"
                else:
                    problem = unescape(seg_)
                continue
            if cur_p == "problem":
                if seg.type == "text" and "答" in str(seg):
                    seg_ = str(seg)
                    answer_index = seg_.index("答")
                    problem += seg_[:answer_index]
                    answer += seg_[answer_index + 1 :]
                    cur_p = "answer"
                else:
                    if seg.type == "at":
                        problem += f"[at:{seg.data['qq']}]"
                    else:
                        problem += (
                            unescape(str(seg)).strip() if seg.type == "text" else seg
                        )
            else:
                if seg.type == "text":
                    answer += unescape(str(seg))
                else:
                    answer += seg
    event.message[0] = event.message[0].data["text"].split("答", maxsplit=1)[-1].strip()
    state["word_scope"] = word_scope
    state["word_type"] = word_type
    state["problem"] = problem
    state["answer"] = answer


@add_word.got("problem_image", prompt="请发送该回答设置的问题图片")
async def _(
    bot: Bot,
    event: MessageEvent,
    word_scope: Optional[str] = ArgStr("word_scope"),
    word_type: Optional[str] = ArgStr("word_type"),
    problem: Optional[str] = ArgStr("problem"),
    answer: Message = Arg("answer"),
    problem_image: Message = Arg("problem_image"),
):
    try:
        if word_type == "正则" and problem:
            problem = unescape(problem)
            try:
                re.compile(problem)
            except re.error:
                await add_word.finish(f"添加词条失败，正则表达式 {problem} 非法！")
        # if str(event.user_id) in bot.config.superusers and isinstance(event, PrivateMessageEvent):
        #     word_scope = "私聊"
        nickname = None
        if problem and bot.config.nickname:
            nickname = [nk for nk in bot.config.nickname if problem.startswith(nk)]
        await WordBank.add_problem_answer(
            str(event.user_id),
            str(event.group_id)
            if isinstance(event, GroupMessageEvent)
            and (not word_scope or word_scope == "私聊")
            else "0",
            scope2int[word_scope] if word_scope else 1,
            type2int[word_type] if word_type else 0,
            problem or problem_image,
            answer,
            nickname[0] if nickname else None,
        )
    except Exception as e:
        if isinstance(e, FinishedException):
            await add_word.finish()
        logger.error(
            f"添加词条 {problem} 错误...",
            "添加词条",
            event.user_id,
            getattr(event, "group_id", None),
            e=e,
        )
        await add_word.finish(f"添加词条 {problem} 发生错误！")
    await add_word.send("添加词条 " + (problem or problem_image) + " 成功！")
    logger.info(
        f"添加词条 {problem} 成功！", "添加词条", event.user_id, getattr(event, "group_id", None)
    )


@delete_word_matcher.handle()
async def _(event: GroupMessageEvent, arg: Message = CommandArg()):
    if not (msg := arg.extract_plain_text().strip()):
        await delete_word_matcher.finish("此命令之后需要跟随指定词条，通过“显示词条“查看")
    result = await delete_word(msg, str(event.group_id))
    await delete_word_matcher.send(result)
    logger.info(f"删除词条:" + msg, "删除词条", event.user_id, event.group_id)


@delete_word_matcher.handle()
async def _(
    bot: Bot,
    event: PrivateMessageEvent,
    arg: Message = CommandArg(),
    cmd: Tuple[str, ...] = Command(),
):
    if str(event.user_id) not in bot.config.superusers:
        await delete_word_matcher.finish("权限不足捏！")
    if not (msg := arg.extract_plain_text().strip()):
        await delete_word_matcher.finish("此命令之后需要跟随指定词条，通过“显示词条“查看")
    result = await delete_word(msg, word_scope=2 if cmd[0] == "删除词条" else 0)
    await delete_word_matcher.send(result)
    logger.info(f"删除词条:" + msg, "删除词条", event.user_id)


@update_word_matcher.handle()
async def _(event: GroupMessageEvent, arg: Message = CommandArg()):
    if not (msg := arg.extract_plain_text().strip()):
        await update_word_matcher.finish("此命令之后需要跟随指定词条，通过“显示词条“查看")
    if len(msg.split()) < 2:
        await update_word_matcher.finish("此命令需要两个参数，请查看帮助")
    result = await update_word(msg, str(event.group_id))
    await update_word_matcher.send(result)
    logger.info(f"更新词条词条:" + msg, "更新词条", event.user_id, event.group_id)


@update_word_matcher.handle()
async def _(
    bot: Bot,
    event: PrivateMessageEvent,
    arg: Message = CommandArg(),
    cmd: Tuple[str, ...] = Command(),
):
    if str(event.user_id) not in bot.config.superusers:
        await delete_word_matcher.finish("权限不足捏！")
    if not (msg := arg.extract_plain_text().strip()):
        await update_word_matcher.finish("此命令之后需要跟随指定词条，通过“显示词条“查看")
    if len(msg.split()) < 2:
        await update_word_matcher.finish("此命令需要两个参数，请查看帮助")
    result = await update_word(msg, word_scope=2 if cmd[0] == "修改词条" else 0)
    await update_word_matcher.send(result)
    logger.info(f"更新词条词条:" + msg, "更新词条", event.user_id)


@show_word_matcher.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    if problem := arg.extract_plain_text().strip():
        id_ = None
        gid = None
        if problem.startswith("id:"):
            id_ = problem.split(":")[-1]
            if (
                not is_number(id_)
                or int(id_) < 0
                or int(id_)
                >= len(await WordBank.get_group_all_problem(str(event.group_id)))
            ):
                await show_word_matcher.finish("id必须为数字且在范围内")
            id_ = int(id_)
        if problem.startswith("gid:"):
            gid = problem.split(":")[-1]
            if (
                not is_number(gid)
                or int(gid) < 0
                or int(gid) >= len(await WordBank.get_problem_by_scope(0))
            ):
                await show_word_matcher.finish("gid必须为数字且在范围内")
            gid = int(gid)
        msg_list = await show_word(problem, id_, gid, None if gid else str(event.group_id))
    else:
        msg_list = await show_word(problem, None, None, str(event.group_id))
    if isinstance(msg_list, str):
        await show_word_matcher.send(msg_list)
    else:
        await bot.send_group_forward_msg(
            group_id=event.group_id, messages=custom_forward_msg(msg_list, bot.self_id)
        )
    logger.info(
        f"查看词条回答:" + problem, "显示词条", event.user_id, getattr(event, "group_id", None)
    )


@show_word_matcher.handle()
async def _(event: PrivateMessageEvent, arg: Message = CommandArg()):
    if problem := arg.extract_plain_text().strip():
        id_ = None
        gid = None
        if problem.startswith("id:"):
            id_ = problem.split(":")[-1]
            if (
                not is_number(id_)
                or int(id_) < 0
                or int(id_) > len(await WordBank.get_problem_by_scope(2))
            ):
                await show_word_matcher.finish("id必须为数字且在范围内")
            id_ = int(id_)
        if problem.startswith("gid:"):
            gid = problem.split(":")[-1]
            if (
                not is_number(gid)
                or int(gid) < 0
                or int(gid) > len(await WordBank.get_problem_by_scope(0))
            ):
                await show_word_matcher.finish("gid必须为数字且在范围内")
            gid = int(gid)
        msg_list = await show_word(
            problem, id_, gid, word_scope=2 if id_ is not None else None
        )
    else:
        msg_list = await show_word(problem, None, None, word_scope=2)
    if isinstance(msg_list, str):
        await show_word_matcher.send(msg_list)
    else:
        t = ""
        for msg in msg_list:
            t += msg + "\n"
        await show_word_matcher.send(t[:-1])
    logger.info(
        f"查看词条回答:" + problem, "显示词条", event.user_id, getattr(event, "group_id", None)
    )
