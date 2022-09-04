import time
from nonebot.internal.adapter.template import MessageTemplate
from nonebot.adapters.onebot.v11 import (
    Message,
    MessageEvent,
    GroupMessageEvent,
    MessageSegment,
)
from services.db_context import db
from typing import Optional, List, Union, Tuple, Any
from datetime import datetime
from configs.path_config import DATA_PATH
import random
from ._config import int2type
from utils.image_utils import get_img_hash
from utils.http_utils import AsyncHttpx
import re

from utils.message_builder import image, face, at
from utils.utils import get_message_img

path = DATA_PATH / "word_bank"


class WordBank(db.Model):
    __tablename__ = "word_bank2"

    id = db.Column(db.Integer(), primary_key=True)
    user_qq = db.Column(db.BigInteger(), nullable=False)
    group_id = db.Column(db.Integer())
    word_scope = db.Column(
        db.Integer(), nullable=False, default=0
    )  # 生效范围 0: 全局 1: 群聊 2: 私聊
    word_type = db.Column(
        db.Integer(), nullable=False, default=0
    )  # 词条类型 0: 完全匹配 1: 模糊 2: 正则 3: 图片
    status = db.Column(db.Boolean(), nullable=False, default=True)  # 词条状态
    problem = db.Column(db.String(), nullable=False)  # 问题，为图片时使用图片hash
    answer = db.Column(db.String(), nullable=False)  # 回答
    placeholder = db.Column(db.String())  # 占位符
    image_path = db.Column(db.String())  # 使用图片作为问题时图片存储的路径
    create_time = db.Column(db.DateTime(), nullable=False)
    update_time = db.Column(db.DateTime(), nullable=False)

    @classmethod
    async def exists(
        cls,
        user_id: Optional[int],
        group_id: Optional[int],
        problem: str,
        answer: Optional[str],
        word_scope: Optional[int] = None,
        word_type: Optional[int] = None,
    ) -> bool:
        """
        说明:
            检测问题是否存在
        参数:
            :param user_id: 用户id
            :param group_id: 群号
            :param problem: 问题
            :param answer: 回答
            :param word_scope: 词条范围
            :param word_type: 词条类型
        """
        query = cls.query.where(cls.problem == problem)
        if user_id:
            query = query.where(cls.user_qq == user_id)
        if group_id:
            query = query.where(cls.group_id == group_id)
        if answer:
            query = query.where(cls.answer == answer)
        if word_type:
            query = query.where(cls.word_type == word_type)
        if word_scope:
            query = query.where(cls.word_scope == word_scope)
        return bool(await query.gino.first())

    @classmethod
    async def add_problem_answer(
        cls,
        user_id: int,
        group_id: Optional[int],
        word_scope: int,
        word_type: int,
        problem: Union[str, Message],
        answer: Union[str, Message],
    ):
        """
        说明:
            添加或新增一个问答
        参数:
            :param user_id: 用户id
            :param group_id: 群号
            :param word_scope: 词条范围,
            :param word_type: 词条类型,
            :param problem: 问题
            :param answer: 回答
        """
        # 对图片做额外处理
        image_path = None
        if word_type == 3:
            url = get_message_img(problem)[0]
            _file = (
                path / "problem" / f"{group_id}" / f"{user_id}_{int(time.time())}.jpg"
            )
            _file.parent.mkdir(exist_ok=True, parents=True)
            await AsyncHttpx.download_file(url, _file)
            problem = str(get_img_hash(_file))
            image_path = f"problem/{group_id}/{user_id}_{int(time.time())}.jpg"
        answer, _list = await cls._answer2format(answer, user_id, group_id)
        if not await cls.exists(user_id, group_id, problem, answer, word_scope, word_type):
            await cls.create(
                user_qq=user_id,
                group_id=group_id,
                word_scope=word_scope,
                word_type=word_type,
                status=True,
                problem=problem,
                answer=answer,
                image_path=image_path,
                placeholder=",".join(_list),
                create_time=datetime.now().replace(microsecond=0),
                update_time=datetime.now().replace(microsecond=0),
            )

    @classmethod
    async def _answer2format(
        cls, answer: Union[str, Message], user_id: int, group_id: int
    ) -> Tuple[str, List[Any]]:
        """
        说明:
            将CQ码转化为占位符
        参数:
            :param answer: 回答内容
            :param user_id: 用户id
            :param group_id: 群号
        """
        if isinstance(answer, str):
            return answer, []
        _list = []
        text = ""
        index = 0
        for seg in answer:
            if isinstance(seg, str):
                text += seg
            elif seg.type == "text":
                text += seg.data["text"]
            elif seg.type == "face":
                text += f"[face:placeholder_{index}]"
                _list.append(seg.data['id'])
            elif seg.type == "at":
                text += f"[at:placeholder_{index}]"
                _list.append(seg.data["qq"])
            else:
                text += f"[image:placeholder_{index}]"
                index += 1
                t = int(time.time())
                _file = path / "answer" / f"{group_id}" / f"{user_id}_{t}.jpg"
                _file.parent.mkdir(exist_ok=True, parents=True)
                await AsyncHttpx.download_file(seg.data["url"], _file)
                _list.append(f"answer/{group_id}/{user_id}_{t}.jpg")
        return text, _list

    @classmethod
    async def _format2answer(
        cls,
        problem: str,
        answer: Union[str, Message],
        user_id: int,
        group_id: int,
        query: Optional["WordBank"] = None,
    ) -> Union[str, Message]:
        """
        说明:
            将占位符转换为CQ码
        参数:
            :param problem: 问题内容
            :param answer: 回答内容
            :param user_id: 用户id
            :param group_id: 群号
        """
        if query:
            answer = query.answer
        else:
            query = await cls.query.where(
                (cls.problem == problem)
                & (cls.user_qq == user_id)
                & (cls.group_id == group_id)
                & (cls.answer == answer)
            ).gino.first()
        if query and query.placeholder:
            type_list = re.findall(rf"\[(.*):placeholder_.*]", answer)
            temp_answer = re.sub(rf"\[(.*):placeholder_.*]", "{}", answer)
            seg_list = []
            for t, p in zip(type_list, query.placeholder.split(",")):
                if t == "image":
                    seg_list.append(image(path / p))
                elif t == "face":
                    seg_list.append(face(p))
                elif t == "at":
                    seg_list.append(at(p))
            return MessageTemplate(temp_answer, Message).format(*seg_list)
        return answer

    @classmethod
    async def check(
        cls,
        event: MessageEvent,
        problem: str,
        word_scope: Optional[int] = None,
        word_type: Optional[int] = None,
    ) -> Optional[Any]:
        """
        说明:
            检测是否包含该问题并获取所有回答
        参数:
            :param event: event
            :param problem: 问题内容
            :param word_scope: 词条范围
            :param word_type: 词条类型
        """
        query = cls.query
        sql_text = "SELECT * FROM public.word_bank2 where 1 = 1"
        # 救命！！没找到gino的正则表达式方法，暂时使用sql语句
        if isinstance(event, GroupMessageEvent):
            if word_scope:
                query = query.where(cls.word_scope == word_scope)
                sql_text += f" and word_scope = {word_scope}"
            else:
                query = query.where(
                    (cls.group_id == event.group_id) | (cls.word_scope == 0)
                )
                sql_text += f" and (group_id = {event.group_id} or word_scope = 0)"
        else:
            query = query.where((cls.word_scope == 2) | (cls.word_scope == 0))
            sql_text += f" and (word_scope = 2 or word_scope = 0)"
            if word_type:
                query = query.where(cls.word_scope == word_type)
                sql_text += f" and word_scope = {word_scope}"
        # 完全匹配
        if await query.where(
            ((cls.word_type == 0) | (cls.word_type == 3)) & (cls.problem == problem)
        ).gino.first():
            return query.where(
                ((cls.word_type == 0) | (cls.word_type == 3)) & (cls.problem == problem)
            )
        # 模糊匹配
        if await db.first(
            db.text(
                sql_text
                + f" and word_type = 1 and :problem like '%' || problem || '%';"
            ),
            problem=problem,
        ):
            return (
                sql_text
                + f" and word_type = 1 and :problem like '%' || problem || '%';"
            )
        # 正则匹配
        if await db.first(
            db.text(
                sql_text
                + f" and word_type = 2 and word_scope != 999 and :problem ~ problem;"
            ),
            problem=problem,
        ):
            return (
                sql_text
                + f" and word_type = 2 and word_scope != 999 and :problem ~ problem;"
            )
        # if await db.first(
        #     db.text(sql_text + f" and word_type = 1 and word_scope != 999 and '{problem}' ~ problem;")
        # ):
        #     return sql_text + f" and word_type = 1 and word_scope != 999 and '{problem}' ~ problem;"
        # return None

    @classmethod
    async def get_answer(
        cls,
        event: MessageEvent,
        problem: str,
        word_scope: Optional[int] = None,
        word_type: Optional[int] = None,
    ) -> Optional[Union[str, Message]]:
        """
        说明:
            根据问题内容获取随机回答
        参数:
            :param event: event
            :param problem: 问题内容
            :param word_scope: 词条范围
            :param word_type: 词条类型
        """
        query = await cls.check(event, problem, word_scope, word_type)
        if query is not None:
            if isinstance(query, str):
                answer_list = await db.all(db.text(query), problem=problem)
                answer = random.choice(answer_list)
                return (
                    await cls._format2answer(answer[6], answer[7], answer[1], answer[2])
                    if answer.placeholder
                    else answer.answer
                )
            else:
                answer_list = await query.gino.all()
                answer = random.choice(answer_list)
                return (
                    await cls._format2answer(
                        problem, answer.answer, answer.user_qq, answer.group_id
                    )
                    if answer.placeholder
                    else answer.answer
                )

    @classmethod
    async def get_problem_all_answer(
        cls,
        problem: str,
        index: Optional[int] = None,
        group_id: Optional[int] = None,
        word_scope: Optional[int] = 0,
    ) -> List[Union[str, Message]]:
        """
        说明:
            获取指定问题所有回答
        参数:
            :param problem: 问题
            :param index: 下标
            :param group_id: 群号
            :param word_scope: 词条范围
        """
        if index is not None:
            if group_id:
                problem = (await cls.query.where(cls.group_id == group_id).gino.all())[
                    index
                ]
            else:
                problem = (
                    await cls.query.where(
                        cls.word_scope == (word_scope or 0)
                    ).gino.all()
                )[index]
            problem = problem.problem
        answer = cls.query.where(cls.problem == problem)
        if group_id:
            answer = answer.where(cls.group_id == group_id)
        return [
            await cls._format2answer("", "", 0, 0, x) for x in (await answer.gino.all())
        ]

    @classmethod
    async def delete_group_problem(
        cls,
        problem: str,
        group_id: int,
        index: Optional[int] = None,
        word_scope: int = 1,
    ):
        """
        说明:
            删除指定问题全部或指定回答
        参数:
            :param problem: 问题文本
            :param group_id: 群号
            :param index: 回答下标
            :param word_scope: 词条范围
        """
        if index is not None:
            if group_id:
                query = await cls.query.where(
                    (cls.group_id == group_id) & (cls.problem == problem)
                ).gino.all()
            else:
                query = await cls.query.where(
                    (cls.word_scope == 0) & (cls.problem == problem)
                ).gino.all()
            await query[index].delete()
        else:
            if group_id:
                await WordBank.delete.where(
                    (cls.group_id == group_id) & (cls.problem == problem)
                ).gino.status()
            else:
                await WordBank.delete.where(
                    (cls.word_scope == word_scope) & (cls.problem == problem)
                ).gino.status()

    @classmethod
    async def update_group_problem(
        cls,
        problem: str,
        replace_str: str,
        group_id: int,
        index: Optional[int] = None,
        word_scope: int = 1,
    ):
        """
        说明:
            修改词条问题
        参数:
            :param problem: 问题
            :param replace_str: 替换问题
            :param group_id: 群号
            :param index: 下标
            :param word_scope: 词条范围
        """
        if index is not None:
            if group_id:
                query = await cls.query.where(
                    (cls.group_id == group_id) & (cls.problem == problem)
                ).gino.all()
            else:
                query = await cls.query.where(
                    (cls.word_scope == word_scope) & (cls.problem == problem)
                ).gino.all()
            await query[index].update(problem=replace_str).apply()
        else:
            if group_id:
                await WordBank.update.values(problem=replace_str).where(
                    (cls.group_id == group_id) & (cls.problem == problem)
                ).gino.status()
            else:
                await WordBank.update.values(problem=replace_str).where(
                    (cls.word_scope == word_scope) & (cls.problem == problem)
                ).gino.status()

    @classmethod
    async def get_group_all_problem(
        cls, group_id: int
    ) -> List[Tuple[Any, Union[MessageSegment, str]]]:
        """
        说明:
            获取群聊所有词条
        参数:
            :param group_id: 群号
        """
        return cls._handle_problem(
            await cls.query.where(cls.group_id == group_id).gino.all()
        )

    @classmethod
    async def get_problem_by_scope(cls, word_scope: int):
        """
        说明:
            通过词条范围获取词条
        参数:
            :param word_scope: 词条范围
        """
        return cls._handle_problem(
            await cls.query.where(cls.word_scope == word_scope).gino.all()
        )

    @classmethod
    async def get_problem_by_type(cls, word_type: int):
        """
        说明:
            通过词条类型获取词条
        参数:
            :param word_type: 词条类型
        """
        return cls._handle_problem(
            await cls.query.where(cls.word_type == word_type).gino.all()
        )

    @classmethod
    def _handle_problem(cls, msg_list: List[Union[str, MessageSegment]]):
        """
            说明:
            格式化处理问题
        参数:
         :param msg_list: 消息列表
        """
        _tmp = []
        problem_list = []
        for q in msg_list:
            if q.problem not in _tmp:
                problem = (
                    q.problem,
                    image(path / q.image_path)
                    if q.image_path
                    else f"[{int2type[q.word_type]}] " + q.problem,
                )
                problem_list.append(problem)
                _tmp.append(q.problem)
        return problem_list

    @classmethod
    async def _move(
        cls,
        user_id: int,
        group_id: Optional[int],
        problem: Union[str, Message],
        answer: Union[str, Message],
        placeholder: str,
    ):
        """
        说明:
            旧词条图片移动方法
        参数:
            :param user_id: 用户id
            :param group_id: 群号
            :param problem: 问题
            :param answer: 回答
            :param placeholder: 占位符
        """
        word_scope = 0
        word_type = 0
        # 对图片做额外处理
        if not await cls.exists(user_id, group_id, problem, answer, word_scope, word_type):
            await cls.create(
                user_qq=user_id,
                group_id=group_id,
                word_scope=word_scope,
                word_type=word_type,
                status=True,
                problem=problem,
                answer=answer,
                image_path=None,
                placeholder=placeholder,
                create_time=datetime.now().replace(microsecond=0),
                update_time=datetime.now().replace(microsecond=0),
            )
