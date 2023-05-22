import random
import time
from pathlib import Path
from typing import Any, List, Optional, Tuple, Union

import nonebot
from nonebot.adapters.onebot.v11 import Message, MessageSegment

from services import logger
from utils.image_utils import text2image
from utils.message_builder import image
from utils.utils import is_number

from ._model import WordBank

driver = nonebot.get_driver()


async def get_problem_str(
    id_: Union[str, int], group_id: Optional[str] = None, word_scope: int = 1
) -> Tuple[str, int]:
    """
    说明:
        通过id获取问题字符串
    参数:
        :param id_: 下标
        :param group_id: 群号
        :param word_scope: 获取类型
    """
    if word_scope in [0, 2]:
        all_problem = await WordBank.get_problem_by_scope(word_scope)
    elif group_id:
        all_problem = await WordBank.get_group_all_problem(group_id)
    else:
        raise Exception("词条类型与群组id不能为空")
    if isinstance(id_, str) and id_.startswith("id:"):
        id_ = id_.split(":")[-1]
    if not is_number(id_) or int(id_) < 0 or int(id_) > len(all_problem):
        return "id必须为数字且在范围内", 999
    return all_problem[int(id_)][0], 200


async def update_word(
    params: str, group_id: Optional[str] = None, word_scope: int = 1
) -> str:
    """
    说明:
        修改群词条
    参数:
        :param params: 参数
        :param group_id: 群号
        :param word_scope: 词条范围
    """
    return await word_handle(params, group_id, "update", word_scope)


async def delete_word(
    params: str, group_id: Optional[str] = None, word_scope: int = 1
) -> str:
    """
    说明:
        删除群词条
    参数:
        :param params: 参数
        :param group_id: 群号
        :param word_scope: 词条范围
    """
    return await word_handle(params, group_id, "delete", word_scope)


async def word_handle(
    params_: str, group_id: Optional[str], type_: str, word_scope: int = 0
) -> str:
    """
    说明:
        词条操作
    参数:
        :param params: 参数
        :param group_id: 群号
        :param type_: 类型
        :param word_scope: 词条范围
    """
    params = params_.split()
    problem = params[0]
    if problem.startswith("id:"):
        problem, code = await get_problem_str(problem, group_id, word_scope)
        if code != 200:
            return problem
    if type_ == "delete":
        index = params[1] if len(params) > 1 else None
        if index:
            answer_num = len(
                await WordBank.get_problem_all_answer(problem, group_id=group_id)
            )
            if not is_number(index) or int(index) < 0 or int(index) > answer_num:
                return "指定回答下标id必须为数字且在范围内"
            index = int(index)
        if await WordBank.delete_group_problem(problem, group_id, index, word_scope):  # type: ignore
            return "删除词条成功"
        return "词条不存在"
    if type_ == "update":
        replace_str = params[1]
        await WordBank.update_group_problem(
            problem, replace_str, group_id, word_scope=word_scope
        )
        return "修改词条成功"
    return "类型错误"


async def show_word(
    problem: str,
    id_: Optional[int],
    gid: Optional[int],
    group_id: Optional[str] = None,
    word_scope: Optional[int] = None,
) -> Union[str, List[Union[str, Message]]]:
    if problem:
        msg_list = []
        if word_scope is not None:
            problem = (await WordBank.get_problem_by_scope(word_scope))[id_][0]  # type: ignore
            id_ = None
        _problem_list = await WordBank.get_problem_all_answer(
            problem,
            id_ if id_ is not None else gid,
            group_id if gid is None else None,
            word_scope,
        )
        for index, msg in enumerate(_problem_list):
            if isinstance(msg, Message):
                tmp = ""
                for seg in msg:
                    tmp += seg
                msg = tmp
            msg_list.append(f"{index}." + msg)
        msg_list = [
            f'词条：{problem or (f"id: {id_}" if id_ is not None else f"gid: {gid}")} 的回答'
        ] + msg_list
        return msg_list  # type: ignore
    else:
        if group_id:
            _problem_list = await WordBank.get_group_all_problem(group_id)
        elif word_scope is not None:
            _problem_list = await WordBank.get_problem_by_scope(word_scope)
        else:
            raise Exception("群组id和词条范围不能都为空")
        global_problem_list = await WordBank.get_problem_by_scope(0)
        if not _problem_list and not global_problem_list:
            return "未收录任何词条.."
        msg_list = await build_message(_problem_list)
        global_msg_list = await build_message(global_problem_list)
        if global_msg_list:
            msg_list.append("###以下为全局词条###")
            msg_list = msg_list + global_msg_list
        return msg_list


async def build_message(_problem_list: List[Tuple[Any, Union[MessageSegment, str]]]):
    index = 0
    str_temp_list = []
    msg_list = []
    temp_str = ""
    for _, problem in _problem_list:
        if len(temp_str.split("\n")) > 50:
            img = await text2image(
                temp_str,
                padding=10,
                color="#f9f6f2",
            )
            msg_list.append(image(b64=img.pic2bs4()))
            temp_str = ""
        if isinstance(problem, str):
            if problem not in str_temp_list:
                str_temp_list.append(problem)
                temp_str += f"{index}. {problem}\n"
        else:
            if temp_str:
                img = await text2image(
                    temp_str,
                    padding=10,
                    color="#f9f6f2",
                )
                msg_list.append(image(b64=img.pic2bs4()))
                temp_str = ""
            msg_list.append(f"{index}." + problem)
        index += 1
    if temp_str:
        img = await text2image(
            temp_str,
            padding=10,
            color="#f9f6f2",
        )
        msg_list.append(image(b64=img.pic2bs4()))
    return msg_list


@driver.on_startup
async def _():
    try:
        from ._old_model import WordBank as OldWordBank
    except ModuleNotFoundError:
        return
    if await WordBank.get_group_all_problem(0):
        return
    logger.info("开始迁移词条 纯文本 数据")
    try:
        word_list = await OldWordBank.get_all()
        new_answer_path = Path() / "data" / "word_bank" / "answer"
        new_problem_path = Path() / "data" / "word_bank" / "problem"
        new_answer_path.mkdir(exist_ok=True, parents=True)
        for word in word_list:
            problem: str = word.problem
            user_id = word.user_id
            group_id = word.group_id
            format_ = word.format
            answer = word.answer
            # 仅对纯文本做处理
            if (
                "[CQ" not in problem
                and "[CQ" not in answer
                and "[_to_me" not in problem
            ):
                if not format_:
                    await WordBank.add_problem_answer(
                        user_id, group_id, 1, 0, problem, answer
                    )
                else:
                    placeholder = []
                    for m in format_.split("<format>"):
                        x = m.split("<_s>")
                        if x[0]:
                            idx, file_name = x[0], x[1]
                            if "jpg" in file_name:
                                answer = answer.replace(
                                    f"[__placeholder_{idx}]",
                                    f"[image:placeholder_{idx}]",
                                )
                                file = (
                                    Path()
                                    / "data"
                                    / "word_bank"
                                    / f"{group_id}"
                                    / file_name
                                )
                                rand = int(time.time()) + random.randint(1, 100000)
                                if file.exists():
                                    new_file = (
                                        new_answer_path
                                        / f"{group_id}"
                                        / f"{user_id}_{rand}.jpg"
                                    )
                                    new_file.parent.mkdir(exist_ok=True, parents=True)
                                    with open(file, "rb") as rb:
                                        with open(new_file, "wb") as wb:
                                            wb.write(rb.read())
                                    # file.rename(new_file)
                                    placeholder.append(
                                        f"answer/{group_id}/{user_id}_{rand}.jpg"
                                    )
                                    await WordBank._move(
                                        user_id,
                                        group_id,
                                        problem,
                                        answer,
                                        ",".join(placeholder),
                                    )
        await WordBank.add_problem_answer(0, 0, 999, 0, "_[OK", "_[OK")
        logger.info("词条 纯文本 数据迁移完成")
        (Path() / "plugins" / "word_bank" / "_old_model.py").unlink()
    except Exception as e:
        logger.warning(f"迁移词条发生错误，如果为首次安装请无视 {type(e)}：{e}")
