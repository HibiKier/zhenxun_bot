from nonebot_plugin_alconna import At
from nonebot_plugin_alconna import At as alcAt
from nonebot_plugin_alconna import Image
from nonebot_plugin_alconna import Image as alcImage
from nonebot_plugin_alconna import Text as alcText
from nonebot_plugin_alconna import UniMessage, UniMsg

from zhenxun.utils.image_utils import ImageTemplate
from zhenxun.utils.message import MessageUtils

from ._model import WordBank


def get_img_and_at_list(message: UniMsg) -> tuple[list[str], list[str]]:
    """获取图片和at数据

    参数:
        message: UniMsg

    返回:
        tuple[list[str], list[str]]: 图片列表，at列表
    """
    img_list, at_list = [], []
    for msg in message:
        if isinstance(msg, alcImage):
            img_list.append(msg.url)
        elif isinstance(msg, alcAt):
            at_list.append(msg.target)
    return img_list, at_list


def get_problem(message: UniMsg) -> str:
    """获取问题内容

    参数:
        message: UniMsg

    返回:
        str: 问题文本
    """
    problem = ""
    a, b = True, True
    for msg in message:
        if isinstance(msg, alcText) or isinstance(msg, str):
            msg = str(msg)
            if "问" in str(msg) and a:
                a = False
                split_text = msg.split("问")
                if len(split_text) > 1:
                    problem += "问".join(split_text[1:])
            if b:
                if "答" in problem:
                    b = False
                    problem = problem.split("答")[0]
                elif "答" in msg and b:
                    b = False
                    # problem += "答".join(msg.split("答")[:-1])
                    problem += msg.split("答")[0]
        if not a and not b:
            break
        if isinstance(msg, alcAt):
            problem += f"[at:{msg.target}]"
    return problem


def get_answer(message: UniMsg) -> UniMessage | None:
    """获取at时回答

    参数:
        message: UniMsg

    返回:
        str: 回答内容
    """
    temp_message = None
    answer = ""
    index = 0
    for msg in message:
        index += 1
        if isinstance(msg, alcText) or isinstance(msg, str):
            msg = str(msg)
            if "答" in msg:
                answer += "答".join(msg.split("答")[1:])
                break
    if answer:
        temp_message = message[index:]
        temp_message.insert(0, alcText(answer))
    return temp_message


class WordBankManage:

    @classmethod
    async def update_word(
        cls,
        replace: str,
        problem: str = "",
        index: int | None = None,
        group_id: str | None = None,
        word_scope: int = 1,
    ) -> tuple[str, str]:
        """修改群词条

        参数:
            params: 参数
            group_id: 群号
            word_scope: 词条范围

        返回:
            tuple[str, str]: 处理消息，替换的旧词条
        """
        return await cls.__word_handle(
            problem, group_id, "update", index, None, word_scope, replace
        )

    @classmethod
    async def delete_word(
        cls,
        problem: str,
        index: int | None = None,
        aid: int | None = None,
        group_id: str | None = None,
        word_scope: int = 1,
    ) -> tuple[str, str]:
        """删除群词条

        参数:
            params: 参数
            index: 指定下标
            aid: 指定回答下标
            group_id: 群号
            word_scope: 词条范围

        返回:
            tuple[str, str]: 处理消息，空
        """
        return await cls.__word_handle(
            problem, group_id, "delete", index, aid, word_scope
        )

    @classmethod
    async def __word_handle(
        cls,
        problem: str,
        group_id: str | None,
        handle_type: str,
        index: int | None = None,
        aid: int | None = None,
        word_scope: int = 0,
        replace_problem: str = "",
    ) -> tuple[str, str]:
        """词条操作

        参数:
            problem: 参数
            group_id: 群号
            handle_type: 类型
            index: 指定回答下标
            aid: 指定回答下标
            word_scope: 词条范围
            replace_problem: 替换问题内容

        返回:
            tuple[str, str]: 处理消息，替换的旧词条
        """
        if index is not None:
            problem, code = await cls.__get_problem_str(index, group_id, word_scope)
            if code != 200:
                return problem, ""
        if handle_type == "delete":
            if index:
                problem, _problem_list = await WordBank.get_problem_all_answer(
                    problem, None, group_id, word_scope
                )
                if not _problem_list:
                    return problem, ""
            if await WordBank.delete_group_problem(problem, group_id, aid, word_scope):  # type: ignore
                return "删除词条成功!", ""
            return "词条不存在", ""
        if handle_type == "update":
            old_problem = await WordBank.update_group_problem(
                problem, replace_problem, group_id, word_scope=word_scope
            )
            return f"修改词条成功!\n{old_problem} -> {replace_problem}", old_problem
        return "类型错误", ""

    @classmethod
    async def __get_problem_str(
        cls, idx: int, group_id: str | None = None, word_scope: int = 1
    ) -> tuple[str, int]:
        """通过id获取问题字符串

        参数:
            idx: 下标
            group_id: 群号
            word_scope: 获取类型
        """
        if word_scope in [0, 2]:
            all_problem = await WordBank.get_problem_by_scope(word_scope)
        elif group_id:
            all_problem = await WordBank.get_group_all_problem(group_id)
        else:
            raise Exception("词条类型与群组id不能为空")
        if idx < 0 or idx >= len(all_problem):
            return "问题下标id必须在范围内", 999
        return all_problem[idx][0], 200

    @classmethod
    async def show_word(
        cls,
        problem: str | None,
        index: int | None = None,
        group_id: str | None = None,
        word_scope: int | None = 1,
    ) -> UniMessage:
        """获取群词条

        参数:
            problem: 问题
            group_id: 群组id
            word_scope: 词条范围
            index: 指定回答下标
        """
        if problem or index != None:
            msg_list = []
            problem, _problem_list = await WordBank.get_problem_all_answer(
                problem,  # type: ignore
                index,
                group_id if group_id is not None else None,
                word_scope,
            )
            if not _problem_list:
                return MessageUtils.build_message(problem)
            for msg in _problem_list:
                _text = str(msg)
                if isinstance(msg, At):
                    _text = f"[at:{msg.target}]"
                elif isinstance(msg, Image):
                    _text = msg.url or msg.path
                elif isinstance(msg, list):
                    _text = []
                    for m in msg:
                        __text = str(m)
                        if isinstance(m, At):
                            __text = f"[at:{m.target}]"
                        elif isinstance(m, Image):
                            # TODO: 显示词条回答图片
                            # __text = (m.data["image"], 30, 30)
                            __text = "[图片]"
                        _text.append(__text)
                    _text = "".join(_text)
                msg_list.append(_text)
            column_name = ["序号", "回答内容"]
            data_list = []
            for index, msg in enumerate(msg_list):
                data_list.append([index, msg])
            template_image = await ImageTemplate.table_page(
                f"词条 {problem} 的回答", None, column_name, data_list
            )
            return MessageUtils.build_message(template_image)
        else:
            result = []
            if group_id:
                _problem_list = await WordBank.get_group_all_problem(group_id)
            elif word_scope is not None:
                _problem_list = await WordBank.get_problem_by_scope(word_scope)
            else:
                raise Exception("群组id和词条范围不能都为空")
            global_problem_list = await WordBank.get_problem_by_scope(0)
            if not _problem_list and not global_problem_list:
                return MessageUtils.build_message("未收录任何词条...")
            column_name = ["序号", "关键词", "匹配类型", "收录用户"]
            data_list = [list(s) for s in _problem_list]
            for i in range(len(data_list)):
                data_list[i].insert(0, i)
            group_image = await ImageTemplate.table_page(
                "群组内词条" if group_id else "私聊词条", None, column_name, data_list
            )
            result.append(group_image)
            if global_problem_list:
                data_list = [list(s) for s in global_problem_list]
                for i in range(len(data_list)):
                    data_list[i].insert(0, i)
                global_image = await ImageTemplate.table_page(
                    "全局词条", None, column_name, data_list
                )
                result.append(global_image)
            return MessageUtils.build_message(result)
