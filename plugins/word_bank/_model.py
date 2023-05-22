import random
import re
import time
import uuid
from datetime import datetime
from typing import Any, List, Optional, Tuple, Union

from nonebot.adapters.onebot.v11 import (
    GroupMessageEvent,
    Message,
    MessageEvent,
    MessageSegment,
)
from nonebot.internal.adapter.template import MessageTemplate
from tortoise import Tortoise, fields
from tortoise.expressions import Q

from configs.path_config import DATA_PATH
from services.db_context import Model
from utils.http_utils import AsyncHttpx
from utils.image_utils import get_img_hash
from utils.message_builder import at, face, image
from utils.utils import get_message_img

from ._config import int2type

path = DATA_PATH / "word_bank"


class WordBank(Model):

    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_id = fields.CharField(255)
    """用户id"""
    group_id = fields.CharField(255, null=True)
    """群聊id"""
    word_scope = fields.IntField(default=0)
    """生效范围 0: 全局 1: 群聊 2: 私聊"""
    word_type = fields.IntField(default=0)
    """词条类型 0: 完全匹配 1: 模糊 2: 正则 3: 图片"""
    status = fields.BooleanField()
    """词条状态"""
    problem = fields.TextField()
    """问题，为图片时使用图片hash"""
    answer = fields.TextField()
    """回答"""
    placeholder = fields.TextField(null=True)
    """占位符"""
    image_path = fields.TextField(null=True)
    """使用图片作为问题时图片存储的路径"""
    to_me = fields.CharField(255, null=True)
    """昵称开头时存储的昵称"""
    create_time = fields.DatetimeField(auto_now=True)
    """创建时间"""
    update_time = fields.DatetimeField(auto_now_add=True)
    """更新时间"""

    class Meta:
        table = "word_bank2"
        table_description = "词条数据库"

    @classmethod
    async def exists(
        cls,
        user_id: Optional[str],
        group_id: Optional[str],
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
        query = cls.filter(problem=problem)
        if user_id:
            query = query.filter(user_id=user_id)
        if group_id:
            query = query.filter(group_id=group_id)
        if answer:
            query = query.filter(answer=answer)
        if word_type is not None:
            query = query.filter(word_type=word_type)
        if word_scope is not None:
            query = query.filter(word_scope=word_scope)
        return bool(await query.first())

    @classmethod
    async def add_problem_answer(
        cls,
        user_id: str,
        group_id: Optional[str],
        word_scope: int,
        word_type: int,
        problem: Union[str, Message],
        answer: Union[str, Message],
        to_me_nickname: Optional[str] = None,
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
            :param to_me_nickname: at真寻名称
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
        if not await cls.exists(
            user_id, group_id, str(problem), answer, word_scope, word_type
        ):
            await cls.create(
                user_id=user_id,
                group_id=group_id,
                word_scope=word_scope,
                word_type=word_type,
                status=True,
                problem=str(problem).strip(),
                answer=answer,
                image_path=image_path,
                placeholder=",".join(_list),
                create_time=datetime.now().replace(microsecond=0),
                update_time=datetime.now().replace(microsecond=0),
                to_me=to_me_nickname,
            )

    @classmethod
    async def _answer2format(
        cls, answer: Union[str, Message], user_id: str, group_id: Optional[str]
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
            placeholder = uuid.uuid1()
            if isinstance(seg, str):
                text += seg
            elif seg.type == "text":
                text += seg.data["text"]
            elif seg.type == "face":
                text += f"[face:placeholder_{placeholder}]"
                _list.append(seg.data["id"])
            elif seg.type == "at":
                text += f"[at:placeholder_{placeholder}]"
                _list.append(seg.data["qq"])
            else:
                text += f"[image:placeholder_{placeholder}]"
                index += 1
                _file = (
                    path
                    / "answer"
                    / f"{group_id or user_id}"
                    / f"{user_id}_{placeholder}.jpg"
                )
                _file.parent.mkdir(exist_ok=True, parents=True)
                await AsyncHttpx.download_file(seg.data["url"], _file)
                _list.append(
                    f"answer/{group_id or user_id}/{user_id}_{placeholder}.jpg"
                )
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
        if not query:
            query = await cls.get_or_none(
                problem=problem,
                user_id=user_id,
                group_id=group_id,
                answer=answer,
            )
        if not answer:
            answer = query.answer  # type: ignore
        if query and query.placeholder:
            type_list = re.findall(rf"\[(.*?):placeholder_.*?]", str(answer))
            temp_answer = re.sub(rf"\[(.*?):placeholder_.*?]", "{}", str(answer))
            seg_list = []
            for t, p in zip(type_list, query.placeholder.split(",")):
                if t == "image":
                    seg_list.append(image(path / p))
                elif t == "face":
                    seg_list.append(face(int(p)))
                elif t == "at":
                    seg_list.append(at(p))
            return MessageTemplate(temp_answer, Message).format(*seg_list)  # type: ignore
        return answer

    @classmethod
    async def check_problem(
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
        query = cls
        if isinstance(event, GroupMessageEvent):
            if word_scope:
                query = query.filter(word_scope=word_scope)
            else:
                query = query.filter(Q(group_id=event.group_id) | Q(word_scope=0))
        else:
            query = query.filter(Q(word_scope=2) | Q(word_scope=0))
            if word_type:
                query = query.filter(word_scope=word_type)
        # 完全匹配
        if data_list := await query.filter(
            Q(Q(word_type=0) | Q(word_type=3)), Q(problem=problem)
        ).all():
            return data_list
        db = Tortoise.get_connection("default")
        # 模糊匹配
        sql = query.filter(word_type=1).sql() + " and POSITION(problem in $1) > 0"
        data_list = await db.execute_query_dict(sql, [problem])
        if data_list:
            return [cls(**data) for data in data_list]
        # 正则
        sql = (
            query.filter(word_type=2, word_scope__not=999).sql() + " and $1 ~ problem;"
        )
        data_list = await db.execute_query_dict(sql, [problem])
        if data_list:
            return [cls(**data) for data in data_list]
        return None

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
        data_list = await cls.check_problem(event, problem, word_scope, word_type)
        if data_list:
            random_answer = random.choice(data_list)
            temp_answer = random_answer.answer
            if random_answer.word_type == 2:
                r = re.search(random_answer.problem, problem)
                has_placeholder = re.search(rf"\$(\d)", random_answer.answer)
                if r and r.groups() and has_placeholder:
                    pats = re.sub(r"\$(\d)", r"\\\1", random_answer.answer)
                    random_answer.answer = re.sub(random_answer.problem, pats, problem)
            return (
                await cls._format2answer(
                    random_answer.problem,
                    random_answer.answer,
                    random_answer.user_id,
                    random_answer.group_id,
                    random_answer,
                )
                if random_answer.placeholder
                else random_answer.answer
            )

    @classmethod
    async def get_problem_all_answer(
        cls,
        problem: str,
        index: Optional[int] = None,
        group_id: Optional[str] = None,
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
                problem_ = (await cls.filter(group_id=group_id).all())[index]
            else:
                problem_ = (await cls.filter(word_scope=(word_scope or 0)).all())[index]
            problem = problem_.problem
        answer = cls.filter(problem=problem)
        if group_id:
            answer = answer.filter(group_id=group_id)
        return [await cls._format2answer("", "", 0, 0, x) for x in (await answer.all())]

    @classmethod
    async def delete_group_problem(
        cls,
        problem: str,
        group_id: Optional[str],
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
        if await cls.exists(None, group_id, problem, None, word_scope):
            if index is not None:
                if group_id:
                    query = await cls.filter(group_id=group_id, problem=problem).all()
                else:
                    query = await cls.filter(word_scope=0, problem=problem).all()
                await query[index].delete()
            else:
                if group_id:
                    await WordBank.filter(group_id=group_id, problem=problem).delete()
                else:
                    await WordBank.filter(
                        word_scope=word_scope, problem=problem
                    ).delete()
            return True
        return False

    @classmethod
    async def update_group_problem(
        cls,
        problem: str,
        replace_str: str,
        group_id: Optional[str],
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
                query = await cls.filter(group_id=group_id, problem=problem).all()
            else:
                query = await cls.filter(word_scope=word_scope, problem=problem).all()
            query[index].problem = replace_str
            await query[index].save(update_fields=["problem"])
        else:
            if group_id:
                await cls.filter(group_id=group_id, problem=problem).update(
                    problem=replace_str
                )
            else:
                await cls.filter(word_scope=word_scope, problem=problem).update(
                    problem=replace_str
                )

    @classmethod
    async def get_group_all_problem(
        cls, group_id: str
    ) -> List[Tuple[Any, Union[MessageSegment, str]]]:
        """
        说明:
            获取群聊所有词条
        参数:
            :param group_id: 群号
        """
        return cls._handle_problem(
            await cls.filter(group_id=group_id).all()  # type: ignore
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
            await cls.filter(word_scope=word_scope).all()  # type: ignore
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
            await cls.filter(word_type=word_type).all()  # type: ignore
        )

    @classmethod
    def _handle_problem(cls, msg_list: List["WordBank"]):
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
        user_id: str,
        group_id: Optional[str],
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
        if not await cls.exists(
            user_id, group_id, problem, answer, word_scope, word_type
        ):
            await cls.create(
                user_id=user_id,
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

    @classmethod
    async def _run_script(cls):
        return [
            "ALTER TABLE word_bank2 ADD to_me varchar(255);",  # 添加 to_me 字段
            "ALTER TABLE word_bank2 ALTER COLUMN create_time TYPE timestamp with time zone USING create_time::timestamp with time zone;",
            "ALTER TABLE word_bank2 ALTER COLUMN update_time TYPE timestamp with time zone USING update_time::timestamp with time zone;",
            "ALTER TABLE word_bank2 RENAME COLUMN user_qq TO user_id;",  # 将user_qq改为user_id
            "ALTER TABLE word_bank2 ALTER COLUMN user_id TYPE character varying(255);",
            "ALTER TABLE word_bank2 ALTER COLUMN group_id TYPE character varying(255);",
        ]
