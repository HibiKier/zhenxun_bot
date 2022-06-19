from utils.utils import get_message_at, is_number, get_message_img
from nonebot.params import CommandArg
from services.log import logger
from configs.path_config import DATA_PATH
from utils.http_utils import AsyncHttpx
from ._data_source import WordBankBuilder
from utils.message_builder import image
from utils.image_utils import text2image
from .message_handle import get_one_answer, get_one_problem, get_one_image_problem, replace_cq
from .model import WordBank
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message
)
from nonebot import on_command
import random
import os
import re
from configs.config import NICKNAME, Config
from models.group_member_info import GroupInfoUser

__zx_plugin_name__ = "词库问答 [Admin]"
__plugin_usage__ = """
usage：
    对指定问题的随机回答，对相同问题可以设置多个不同回答
    删除词条后每个词条的id可能会变化，请查看后再删除
    指令：
        添加词条 ?[模糊/关键字|词]...答...：添加问答词条，可重复添加相同问题的不同回答
        删除词条 [问题/下标] ?[下标]：删除指定词条指定或全部回答
        修改词条 [问题/下标] ?[下标/新回答] [新回答]：修改指定词条指定回答默认修改为第一条
        查看词条 ?[问题/下标]：查看全部词条或对应词条回答
        示例：添加词条问谁是萝莉答是我
        示例：删除词条 谁是萝莉
        示例：删除词条 谁是萝莉 0
        示例：删除词条 id:0
        示例：修改词条 谁是萝莉 是你
        示例：修改词条 谁是萝莉 0 是你
        示例：修改词条 id:0 是你
        示例：查看词条
        示例：查看词条 谁是萝莉
        示例：查看词条 id:0
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

add_word = on_command("添加词条", priority=5, block=True)

delete_word = on_command("删除词条", priority=5, block=True)

update_word = on_command("修改词条", priority=5, block=True)

show_word = on_command("显示词条", aliases={"查看词条"}, priority=5, block=True)


@add_word.handle()
async def _(event: GroupMessageEvent, arg: Message = CommandArg()):
    msg = str(arg)
    r = re.search(r"问(.+)\s?答([\s\S]*)", msg)
    if not r:
        await add_word.finish("未检测到词条问题...")
    problem = r.group(1).strip()
    if not problem:
        await add_word.finish("未检测到词条问题...")
    answer = msg.split("答", maxsplit=1)[-1]
    if not answer:
        await add_word.finish("未检测到词条回答...")
    idx = 0
    _problem = problem
    search_type = 0
    if re.search("^关键字|词(.*)", msg):
        search_type = 1
    elif re.search("^模糊(.*)", msg):
        search_type = 2
    _builder = await get__builder(event, _problem, answer, idx)
    if await _builder.save(search_type):
        logger.info(f"已保存词条 问：{_builder.problem} 答：{answer}")
        await add_word.send("已保存词条：" + _builder.problem)
    else:
        await delete_word.send("保存失败，可能是回答重复")


@delete_word.handle()
async def _(event: GroupMessageEvent, arg: Message = CommandArg()):
    msg = str(arg)
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
        _problem, problem = await get_one_problem(event, problem)
        if answer := await WordBank.delete_problem_answer(
                event.user_id, event.group_id, _problem, index
        ):

            await delete_word.send(Message(
                "删除词条成功：\n问" + await replace_cq(event.group_id, problem, False) + f"\n回答：\n" + await replace_cq(
                    event.group_id, answer, False) + "\n"))
            logger.info(
                f"(USER {event.user_id}, GROUP "
                f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
                f" 删除词条: {problem}"
            )
        else:
            await delete_word.send("删除词条：" + problem + "失败，可能该词条不存在")
    except IndexError:
        await delete_word.send("指定下标错误...请通过查看词条来确定..")


@update_word.handle()
async def _(event: GroupMessageEvent, arg: Message = CommandArg()):
    msg = str(arg)
    if not msg:
        await update_word.finish("此命令之后需要跟随指定词条，通过“显示词条“查看")
    index = None
    new_answer = None
    problem = None
    _sp_msg = msg.split()
    len_msg = len(_sp_msg)
    if 1 < len_msg:
        problem = "".join(_sp_msg[0])
        if len_msg == 3:
            if is_number(_sp_msg[1]):
                index = int(_sp_msg[1])
            new_answer = "".join(_sp_msg[2:])
        else:
            new_answer = "".join(_sp_msg[1:])
    else:
        await update_word.finish("此命令之后需要跟随修改内容")
    idx = 0
    _problem = problem
    _builder = await get__builder(event, _problem, new_answer, idx)

    try:
        if await _builder.update(index):
            await update_word.send(f"修改词条成功：" + _builder.problem)
            logger.info(
                f"(USER {event.user_id}, GROUP "
                f"{event.group_id if isinstance(event, GroupMessageEvent) else 'private'})"
                f" 修改词条: {problem}"
            )
        else:
            await update_word.send(f"修改词条：" + _builder.problem + f"失败，可能该词条不存在")
    except IndexError:
        await update_word.send("指定下标错误...请通过查看词条来确定..")


@show_word.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    msg = str(arg).strip()
    if not msg:
        _problem_list = await WordBank.get_group_all_problem(event.group_id)
        if not _problem_list:
            await show_word.finish("该群未收录任replace_cq何词条..")
        _problem_list = [f"\t{i}. {await replace_cq(event.group_id, x)}" for i, x in enumerate(_problem_list)]
        long_problem_list = len(_problem_list)
        max_line = Config.get_config("word_bank", "WORD_BANK_MIX")
        if long_problem_list > max_line:
            pic_list = []
            mes_list = []
            img_nu = long_problem_list // max_line
            one_msg = "该群已收录的词条："
            await show_word.send(one_msg)
            for i in range(img_nu + 1):
                if _problem_list:
                    one_img = image(
                        b64=(await text2image("\n".join(_problem_list[:max_line]),
                                              padding=10,
                                              color="#f9f6f2",
                                              )).pic2bs4()
                    )
                    if img_nu > 2:
                        pic_list.append(one_img)
                    else:
                        await show_word.send(one_img)
                del _problem_list[:max_line]
            if pic_list:
                for img in pic_list:
                    data = {
                        "type": "node",
                        "data": {"name": f"{NICKNAME}", "uin": f"{bot.self_id}", "content": img},
                    }
                    mes_list.append(data)
                await bot.send_group_forward_msg(group_id=event.group_id, messages=mes_list)
        else:
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
        _answer_list = []
        if msg.startswith("id:"):
            x = msg.split(":")[-1]
            if not is_number(x) or int(x) < 0:
                return await delete_word.finish("id必须为数字且符合规范！")
            p = await WordBank.get_group_all_problem(event.group_id)
            if p:
                _problem = p[int(x)]
                _answer_list = await WordBank.get_group_all_answer(event.group_id, _problem)
                msg += '问' + await get_one_image_problem(event, _problem)
        else:
            _problem, msg = await get_one_problem(event, msg)
            _answer_list = await WordBank.get_group_all_answer(event.group_id, _problem)
        if not _answer_list:
            await show_word.send("未收录该词条...")

        else:
            # 解析图片和@
            _answer_img_nu_list = [await get_one_answer(event, format, answer, False) for answer, format in
                                   _answer_list]
            word_nu = len(_answer_img_nu_list)
            img_nu = 0
            answer = "词条" + msg + "\n回答："
            for i, x, in enumerate(_answer_img_nu_list):
                r = re.findall(rf"\[CQ:image,file=", str(x))
                if r:
                    img_nu += len(r)
                answer += "\n" + f"{i}." + x
            if (img_nu > 2 and word_nu > 5) or word_nu > 10 or img_nu > 4:
                data = {
                    "type": "node",
                    "data": {"name": f"{NICKNAME}", "uin": f"{bot.self_id}", "content": answer},
                }
                await bot.send_group_forward_msg(group_id=event.group_id, messages=data)
            else:
                await show_word.send(answer)
            # await show_word.send(f"词条 {msg} 回答：\n" + "\n".join(_answer_list))


async def get__builder(event, _problem: str, answer: str, idx: int):
    (data_dir / f"{event.group_id}").mkdir(exist_ok=True, parents=True)
    (data_dir / f"{event.group_id}" / "problem").mkdir(exist_ok=True, parents=True)
    _builder = WordBankBuilder(event.user_id, event.group_id, _problem)
    problem = ''
    _p = _problem
    for at_ in get_message_at(event.json()):
        r = re.search(rf"\[CQ:at,qq={at_}]", answer)
        if r:
            answer = answer.replace(f"[CQ:at,qq={at_}]", f"[__placeholder_{idx}]", 1)
            _builder.set_placeholder(idx, at_)
            idx += 1
        r_problem = re.search(rf"\[CQ:at,qq={at_}]", _problem)
        if r_problem:
            q = await GroupInfoUser.get_member_info(
                int(at_), event.group_id)
            problem += _p[: _p.find(f"[CQ:at,qq={at_}]")] + "@" + q.user_name
            _p = _p[_p.find(f"[CQ:at,qq={at_}]") + len(f"[CQ:at,qq={at_}]"):]
    for img in get_message_img(event.json()):
        _x = img.split("?")[0]
        _x_list = img.split("?")
        r = re.search(rf"\[CQ:image,file=(.*),url={_x}.*?]", answer)
        if r:
            rand = random.randint(1, 10000) + random.randint(1, 114514)
            for _ in range(10):
                if f"__placeholder_{rand}_{idx}.jpg" not in os.listdir(data_dir / f"{event.group_id}"):
                    break
                rand = random.randint(1, 10000) + random.randint(1, 114514)
            strinfo = re.compile(f"\[CQ:image,file={r.group(1)},.*url={_x_list[0]}\?{_x_list[1]}.*?]")
            answer = strinfo.sub(f"[__placeholder_{idx}]", answer)
            await AsyncHttpx.download_file(
                img, data_dir / f"{event.group_id}" / f"__placeholder_{rand}_{idx}.jpg"
            )
            _builder.set_placeholder(idx, f"__placeholder_{rand}_{idx}.jpg")
            idx += 1
        r_problem = re.search(rf"\[CQ:image,file=(.*?)(,subType=\d)?,url={_x}.*?]", _p)
        if r_problem:
            strinfo = re.compile(f"(,subType=\d)?,url={_x_list[0]}\?{_x_list[1]}.*?]")
            _problem = strinfo.sub(f"]", _problem)
            _p = strinfo.sub(f"]", _p)
            problem += _p[: _p.find(f"[CQ:image,file={r_problem.group(1)}]")] + image(img)
            _p = _p[_p.find(f"[CQ:image,file={r_problem.group(1)}]") + len(f"[CQ:image,file={r_problem.group(1)}]"):]
            problem_img = r_problem.group(1)
            if f"{problem_img}.jpg" not in os.listdir(data_dir / f"{event.group_id}" / f"problem"):
                await AsyncHttpx.download_file(
                    img, data_dir / f"{event.group_id}" / f"problem" / f"{problem_img}.jpg"
                )
    _builder.set_answer(answer)
    _builder.set_problem(_problem)
    _builder.problem = problem + _p
    return _builder
