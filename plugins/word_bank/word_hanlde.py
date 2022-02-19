from utils.utils import get_message_at, is_number, get_message_img
from nonebot.params import CommandArg
from services.log import logger
from configs.path_config import DATA_PATH
from utils.http_utils import AsyncHttpx
from ._data_source import WordBankBuilder
from configs.config import Config
from utils.message_builder import image
from utils.image_utils import text2image
from .model import WordBank
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message
)
from nonebot.typing import T_State
from nonebot import on_command
import random
import os
import re

__zx_plugin_name__ = "词库问答 [Admin]"
__plugin_usage__ = """
usage：
    对指定问题的随机回答，对相同问题可以设置多个不同回答
    删除词条后每个词条的id可能会变化，请查看后再删除
    指令：
        添加词条问...答...：添加问答词条，可重复添加相同问题的不同回答
        删除词条 [问题/下标] ?[下标]：删除指定词条指定或全部回答
        查看词条 ?[问题/下标]：查看全部词条或对应词条回答
        示例：添加词条问谁是萝莉答是我
        示例：删除词条 谁是萝莉
        示例：删除词条 谁是萝莉 0
        示例：删除词条 id:0
        示例：查看词条
        示例：查看词条 谁是萝莉
        示例：查看词条 id:0
""".strip()
__plugin_des__ = "自定义词条内容随机回复"
__plugin_cmd__ = [
    "添加词条问...答..",
    "删除词条 [问题/下标] ?[下标]",
    "查看词条 ?[问题/下标]",
]
__plugin_version__ = 0.1
__plugin_author__ = "HibiKier"
__plugin_settings__ = {
    "admin_level": Config.get_config("word_bank", "WORD_BANK_LEVEL"),
    "cmd": ["词库问答", "添加词条", "删除词条", "查看词条"],
}

data_dir = DATA_PATH / "word_bank"
data_dir.mkdir(parents=True, exist_ok=True)


add_word = on_command("添加词条", priority=5, block=True)

delete_word = on_command("删除词条", priority=5, block=True)

show_word = on_command("显示词条", aliases={"查看词条"}, priority=5, block=True)


@add_word.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State, arg: Message = CommandArg()):
    msg = str(arg)
    r = re.search(r"^问(.+)\s?答([\s\S]*)", msg)
    if not r:
        await add_word.finish("未检测到词条问题...")
    problem = r.group(1).strip()
    if not problem:
        await add_word.finish("未检测到词条问题...")
    answer = msg.split("答", maxsplit=1)[-1]
    if not answer:
        await add_word.finish("未检测到词条回答...")
    idx = 0
    for n in bot.config.nickname:
        if n and problem.startswith(n):
            _problem = f"[_to_me|{n}]" + problem[len(n) :]
            break
    else:
        _problem = problem
    (data_dir / f"{event.group_id}").mkdir(exist_ok=True, parents=True)
    _builder = WordBankBuilder(event.user_id, event.group_id, _problem)
    for at_ in get_message_at(event.json()):
        r = re.search(rf"\[CQ:at,qq={at_}]", answer)
        if r:
            answer = answer.replace(f"[CQ:at,qq={at_}]", f"[__placeholder_{idx}]", 1)
            _builder.set_placeholder(idx, at_)
            idx += 1
    for img in get_message_img(event.json()):
        _x = img.split("?")[0]
        r = re.search(rf"\[CQ:image,file=(.*),url={_x}.*?]", answer)
        if r:
            rand = random.randint(1, 10000) + random.randint(1, 114514)
            for _ in range(10):
                if f"__placeholder_{rand}_{idx}.jpg" not in os.listdir(data_dir / f"{event.group_id}"):
                    break
                rand = random.randint(1, 10000) + random.randint(1, 114514)
            for i in range(3):
                answer = answer.replace(f",subType={i}", "")
            answer = answer.replace(
                rf"[CQ:image,file={r.group(1)},url={img}]",
                f"[__placeholder_{idx}]",
            )
            await AsyncHttpx.download_file(
                img, data_dir / f"{event.group_id}" / f"__placeholder_{rand}_{idx}.jpg"
            )
            _builder.set_placeholder(idx, f"__placeholder_{rand}_{idx}.jpg")
            idx += 1
    _builder.set_answer(answer)
    await _builder.save()
    logger.info(f"已保存词条 问：{problem} 答：{msg}")
    await add_word.send(f"已保存词条：{problem}")


@delete_word.handle()
async def _(event: GroupMessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    if not msg:
        await delete_word.finish("此命令之后需要跟随指定词条，通过“显示词条“查看")
    index = None
    _sp_msg = msg.split()
    if len(_sp_msg) > 1:
        if is_number(_sp_msg[-1]):
            index = int(_sp_msg[-1])
            msg = " ".join(_sp_msg[:-1])
    problem = msg
    if problem.startswith("id:"):
        x = problem.split(":")[-1]
        if not is_number(x) or int(x) < 0:
            await delete_word.finish("id必须为数字且符合规范！")
        p = await WordBank.get_group_all_problem(event.group_id)
        if p:
            problem = p[int(x)]
    try:
        if answer := await WordBank.delete_problem_answer(
            event.user_id, event.group_id, problem, index
        ):
            await delete_word.send(f"删除词条成功：{problem}\n回答：\n{answer}")
            logger.info(
                f"(USER {event.user_id}, GROUP "
                f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
                f" 删除词条: {problem}"
            )
        else:
            await delete_word.send(f"删除词条：{problem} 失败，可能该词条不存在")
    except IndexError:
        await delete_word.send("指定下标错误...请通过查看词条来确定..")


@show_word.handle()
async def _(event: GroupMessageEvent, arg: Message = CommandArg()):
    msg = arg.extract_plain_text().strip()
    if not msg:
        _problem_list = await WordBank.get_group_all_problem(event.group_id)
        if not _problem_list:
            await show_word.finish("该群未收录任何词条..")
        _problem_list = [f"\t{i}. {x}" for i, x in enumerate(_problem_list)]
        await show_word.send(
            image(
                b64=(await text2image(
                    "该群已收录的词条：\n\n" + "\n".join(_problem_list),
                    padding=10,
                    color="#f9f6f2",
                )).pic2bs4()
            )
        )
    else:
        _answer_list = await WordBank.get_group_all_answer(event.group_id, msg)
        if not _answer_list:
            await show_word.send("未收录该词条...")
        else:
            _answer_list = [f"{i}. {x}" for i, x in enumerate(_answer_list)]
            await show_word.send(f"词条 {msg} 回答：\n" + "\n".join(_answer_list))
