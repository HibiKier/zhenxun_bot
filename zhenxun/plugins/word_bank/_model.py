import re
import uuid
import random
from typing import Any
from datetime import datetime
from typing_extensions import Self

from tortoise.expressions import Q
from tortoise import Tortoise, fields
from nonebot_plugin_alconna import UniMessage
from nonebot_plugin_alconna import At as alcAt
from nonebot_plugin_alconna import Text as alcText
from nonebot_plugin_alconna import Image as alcImage

from zhenxun.services.db_context import Model
from zhenxun.utils.message import MessageUtils
from zhenxun.utils.http_utils import AsyncHttpx
from zhenxun.configs.path_config import DATA_PATH
from zhenxun.utils.image_utils import get_img_hash

from ._config import WordType, ScopeType, int2type

path = DATA_PATH / "word_bank"


class WordBank(Model):
    id = fields.IntField(pk=True, generated=True, auto_increment=True)
    """自增id"""
    user_id = fields.CharField(255)
    """用户id"""
    group_id = fields.CharField(255, null=True)
    """群聊id"""
    word_scope = fields.IntField(default=ScopeType.GLOBAL.value)
    """生效范围 0: 全局 1: 群聊 2: 私聊"""
    word_type = fields.IntField(default=WordType.EXACT.value)
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
    platform = fields.CharField(255, default="qq")
    """平台"""
    author = fields.CharField(255, null=True, default="")
    """收录人"""

    class Meta:  # type: ignore
        table = "word_bank2"
        table_description = "词条数据库"

    @classmethod
    async def exists(  # type: ignore
        cls,
        user_id: str | None,
        group_id: str | None,
        problem: str,
        answer: str | None,
        word_scope: ScopeType | None = None,
        word_type: WordType | None = None,
    ) -> bool:
        """检测问题是否存在

        参数:
            user_id: 用户id
            group_id: 群号
            problem: 问题
            answer: 回答
            word_scope: 词条范围
            word_type: 词条类型
        """
        query = cls.filter(problem=problem)
        if user_id:
            query = query.filter(user_id=user_id)
        if group_id:
            query = query.filter(group_id=group_id)
        if answer:
            query = query.filter(answer=answer)
        if word_type is not None:
            query = query.filter(word_type=word_type.value)
        if word_scope is not None:
            query = query.filter(word_scope=word_scope.value)
        return await query.exists()

    @classmethod
    async def add_problem_answer(
        cls,
        user_id: str,
        group_id: str | None,
        word_scope: ScopeType,
        word_type: WordType,
        problem: str,
        answer: list[str | alcText | alcAt | alcImage],
        to_me_nickname: str | None = None,
        platform: str = "",
        author: str = "",
    ):
        """添加或新增一个问答

        参数:
            user_id: 用户id
            group_id: 群号
            word_scope: 词条范围,
            word_type: 词条类型,
            problem: 问题, 为图片时是URl
            answer: 回答
            to_me_nickname: at真寻名称
            platform: 所属平台
            author: 收录人id
        """
        # 对图片做额外处理
        image_path = None
        if word_type == WordType.IMAGE:
            _uuid = uuid.uuid1()
            _file = path / "problem" / f"{group_id}" / f"{user_id}_{_uuid}.jpg"
            _file.parent.mkdir(exist_ok=True, parents=True)
            await AsyncHttpx.download_file(problem, _file)
            problem = get_img_hash(_file)
            image_path = f"problem/{group_id}/{user_id}_{_uuid}.jpg"
        new_answer, placeholder_list = await cls._answer2format(
            answer, user_id, group_id
        )
        if not await cls.exists(
            user_id, group_id, problem, new_answer, word_scope, word_type
        ):
            await cls.create(
                user_id=user_id,
                group_id=group_id,
                word_scope=word_scope.value,
                word_type=word_type.value,
                status=True,
                problem=str(problem).strip(),
                answer=new_answer,
                image_path=image_path,
                placeholder=",".join(placeholder_list),
                create_time=datetime.now().replace(microsecond=0),
                update_time=datetime.now().replace(microsecond=0),
                to_me=to_me_nickname,
                platform=platform,
                author=author,
            )

    @classmethod
    async def _answer2format(
        cls,
        answer: list[str | alcText | alcAt | alcImage],
        user_id: str,
        group_id: str | None,
    ) -> tuple[str, list[Any]]:
        """将特殊字段转化为占位符，图片，at等

        参数:
            answer: 回答内容
            user_id: 用户id
            group_id: 群号

        返回:
            tuple[str, list[Any]]: 替换后的文本回答内容，占位符
        """
        placeholder_list = []
        text = ""
        index = 0
        for seg in answer:
            placeholder = uuid.uuid1()
            if isinstance(seg, str):
                text += seg
            elif isinstance(seg, alcText):
                text += seg.text
            elif seg.type == "face":  # TODO: face貌似无用...
                text += f"[face:placeholder_{placeholder}]"
                placeholder_list.append(seg.data["id"])
            elif isinstance(seg, alcAt):
                text += f"[at:placeholder_{placeholder}]"
                placeholder_list.append(seg.target)
            elif isinstance(seg, alcImage) and seg.url:
                text += f"[image:placeholder_{placeholder}]"
                index += 1
                _file = (
                    path
                    / "answer"
                    / f"{group_id or user_id}"
                    / f"{user_id}_{placeholder}.jpg"
                )
                _file.parent.mkdir(exist_ok=True, parents=True)
                await AsyncHttpx.download_file(seg.url, _file)
                placeholder_list.append(
                    f"answer/{group_id or user_id}/{user_id}_{placeholder}.jpg"
                )
        return text, placeholder_list

    @classmethod
    async def _format2answer(
        cls,
        problem: str,
        answer: str,
        user_id: int,
        group_id: int,
        query: Self | None = None,
    ) -> UniMessage:
        """将占位符转换为实际内容

        参数:
            problem: 问题内容
            answer: 回答内容
            user_id: 用户id
            group_id: 群组id
        """
        if not query:
            query = await cls.get_or_none(
                problem=problem,
                user_id=user_id,
                group_id=group_id,
                answer=answer,
            )
        if not answer:
            answer = str(query.answer)  # type: ignore
        if query and query.placeholder:
            type_list = re.findall(r"\[(.*?):placeholder_.*?]", answer)
            answer_split = re.split(r"\[.*:placeholder_.*?]", answer)
            placeholder_split = query.placeholder.split(",")
            result_list = []
            for index, ans in enumerate(answer_split):
                result_list.append(ans)
                if index < len(type_list):
                    t = type_list[index]
                    p = placeholder_split[index]
                    if t == "at":
                        result_list.append(alcAt(flag="user", target=p))
                    elif t == "image":
                        result_list.append(path / p)
            return MessageUtils.build_message(result_list)
        return MessageUtils.build_message(answer)

    @classmethod
    async def check_problem(
        cls,
        group_id: str | None,
        problem: str,
        word_scope: ScopeType | None = None,
        word_type: WordType | None = None,
    ) -> Any:
        """检测是否包含该问题并获取所有回答

        参数:
            group_id: 群组id
            problem: 问题内容
            word_scope: 词条范围
            word_type: 词条类型
        """
        query = cls
        if group_id:
            if word_scope:
                query = query.filter(word_scope=word_scope.value)
            else:
                query = query.filter(
                    Q(group_id=group_id) | Q(word_scope=WordType.EXACT.value)
                )
        else:
            query = query.filter(
                Q(word_scope=ScopeType.PRIVATE.value)
                | Q(word_scope=ScopeType.GLOBAL.value)
            )
            if word_type:
                query = query.filter(word_scope=word_type.value)
        # 完全匹配
        if data_list := await query.filter(
            Q(Q(word_type=WordType.EXACT.value) | Q(word_type=WordType.IMAGE.value)),
            Q(problem=problem),
        ).all():
            return data_list
        db = Tortoise.get_connection("default")
        # 模糊匹配
        sql = (
            query.filter(word_type=WordType.FUZZY.value).sql()
            + " and POSITION(problem in $1) > 0"
        )
        data_list = await db.execute_query_dict(sql, [problem])
        if data_list:
            return [cls(**data) for data in data_list]
        # 正则
        sql = (
            query.filter(word_type=WordType.REGEX.value, word_scope__not=999).sql()
            + " and $1 ~ problem;"
        )
        data_list = await db.execute_query_dict(sql, [problem])
        return [cls(**data) for data in data_list] if data_list else None

    @classmethod
    async def get_answer(
        cls,
        group_id: str | None,
        problem: str,
        word_scope: ScopeType | None = None,
        word_type: WordType | None = None,
    ) -> UniMessage | None:
        """根据问题内容获取随机回答

        参数:
            user_id: 用户id
            group_id: 群组id
            problem: 问题内容
            word_scope: 词条范围
            word_type: 词条类型
        """
        data_list = await cls.check_problem(group_id, problem, word_scope, word_type)
        if data_list:
            random_answer = random.choice(data_list)
            if random_answer.word_type == WordType.REGEX:
                r = re.search(random_answer.problem, problem)
                has_placeholder = re.search(r"\$(\d)", random_answer.answer)
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
                else MessageUtils.build_message(random_answer.answer)
            )

    @classmethod
    async def get_problem_all_answer(
        cls,
        problem: str,
        index: int | None = None,
        group_id: str | None = None,
        word_scope: ScopeType | None = ScopeType.GLOBAL,
    ) -> tuple[str, list[UniMessage]]:
        """获取指定问题所有回答

        参数:
            problem: 问题
            index: 下标
            group_id: 群号
            word_scope: 词条范围

        返回:
            tuple[str, list[UniMessage]]: 问题和所有回答
        """
        if index is not None:
            # TODO: group_by和order_by不能同时使用
            if group_id and word_scope != ScopeType.GLOBAL:
                _problem = (
                    await cls.filter(group_id=group_id).order_by("create_time")
                    # .group_by("problem")
                    .values_list("problem", flat=True)
                )
            else:
                _problem = (
                    await cls.filter(
                        word_scope=(word_scope or ScopeType.GLOBAL).value
                    ).order_by("create_time")
                    # .group_by("problem")
                    .values_list("problem", flat=True)
                )
            # if index is None and problem not in _problem:
            #     return "词条不存在...", []
            sort_problem = []
            for p in _problem:
                if p not in sort_problem:
                    sort_problem.append(p)
            if index > len(sort_problem) - 1:
                return "下标错误，必须小于问题数量...", []
            problem = sort_problem[index]  # type: ignore
        f = cls.filter(
            problem=problem, word_scope=(word_scope or ScopeType.GLOBAL).value
        )
        if group_id:
            f = f.filter(group_id=group_id)
        answer_list = await f.all()
        if not answer_list:
            return "词条不存在...", []
        return problem, [await cls._format2answer("", "", 0, 0, a) for a in answer_list]

    @classmethod
    async def delete_group_problem(
        cls,
        problem: str,
        group_id: str | None,
        index: int | None = None,
        word_scope: ScopeType = ScopeType.GROUP,
    ):
        """删除指定问题全部或指定回答

        参数:
            problem: 问题文本
            group_id: 群号
            index: 回答下标
            word_scope: 词条范围
        """
        if await cls.exists(None, group_id, problem, None, word_scope):
            if index is not None:
                if group_id:
                    query = await cls.filter(
                        group_id=group_id, problem=problem, word_scope=word_scope.value
                    ).all()
                else:
                    query = await cls.filter(
                        word_scope=word_scope.value, problem=problem
                    ).all()
                await query[index].delete()
            else:
                if group_id:
                    await WordBank.filter(
                        group_id=group_id, problem=problem, word_scope=word_scope.value
                    ).delete()
                else:
                    await WordBank.filter(
                        word_scope=word_scope.value, problem=problem
                    ).delete()
            return True
        return False

    @classmethod
    async def update_group_problem(
        cls,
        problem: str,
        replace_str: str,
        group_id: str | None,
        index: int | None = None,
        word_scope: ScopeType = ScopeType.GROUP,
    ) -> str:
        """修改词条问题

        参数:
            problem: 问题
            replace_str: 替换问题
            group_id: 群号
            index: 问题下标
            word_scope: 词条范围

        返回:
            str: 修改前的问题
        """
        if index is not None:
            if group_id:
                query = await cls.filter(group_id=group_id, problem=problem).all()
            else:
                query = await cls.filter(
                    word_scope=word_scope.value, problem=problem
                ).all()
            tmp = query[index].problem
            query[index].problem = replace_str
            await query[index].save(update_fields=["problem"])
            return tmp
        else:
            if group_id:
                await cls.filter(group_id=group_id, problem=problem).update(
                    problem=replace_str
                )
            else:
                await cls.filter(word_scope=word_scope.value, problem=problem).update(
                    problem=replace_str
                )
            return problem

    @classmethod
    async def get_group_all_problem(cls, group_id: str) -> list[tuple[Any | str]]:
        """获取群聊所有词条

        参数:
            group_id: 群号
        """
        return cls._handle_problem(
            await cls.filter(group_id=group_id).order_by("create_time").all()  # type: ignore
        )

    @classmethod
    async def get_problem_by_scope(cls, word_scope: ScopeType):
        """通过词条范围获取词条

        参数:
            word_scope: 词条范围
        """
        return cls._handle_problem(
            await cls.filter(word_scope=word_scope.value).order_by("create_time").all()  # type: ignore
        )

    @classmethod
    async def get_problem_by_type(cls, word_type: int):
        """通过词条类型获取词条

        参数:
            word_type: 词条类型
        """
        return cls._handle_problem(
            await cls.filter(word_type=word_type).order_by("create_time").all()  # type: ignore
        )

    @classmethod
    def __type2int(cls, value: int) -> str:
        for key, member in WordType.__members__.items():
            if member.value == value:
                return key
        return ""

    @classmethod
    def _handle_problem(cls, problem_list: list["WordBank"]):
        """格式化处理问题

        参数:
            msg_list: 消息列表
        """
        _tmp = []
        result_list = []
        for q in problem_list:
            if q.problem not in _tmp:
                word_type = cls.__type2int(q.word_type)
                # TODO: 获取收录人名称
                problem = (
                    (path / q.image_path, 30, 30) if q.image_path else q.problem,
                    int2type[word_type],
                    # q.author,
                    "-",
                )
                result_list.append(problem)
                _tmp.append(q.problem)
        return result_list

    @classmethod
    async def _move(
        cls,
        user_id: str,
        group_id: str | None,
        problem: str,
        answer: str,
        placeholder: str,
    ):
        """旧词条图片移动方法

        参数:
            user_id: 用户id
            group_id: 群号
            problem: 问题
            answer: 回答
            placeholder: 占位符
        """
        word_scope = ScopeType.GLOBAL
        word_type = WordType.EXACT
        # 对图片做额外处理
        if not await cls.exists(
            user_id, group_id, problem, answer, word_scope, word_type
        ):
            await cls.create(
                user_id=user_id,
                group_id=group_id,
                word_scope=word_scope.value,
                word_type=word_type.value,
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
            (
                "ALTER TABLE word_bank2 ALTER COLUMN create_time TYPE timestamp"
                " with time zone USING create_time::timestamp with time zone;"
            ),
            (
                "ALTER TABLE word_bank2 ALTER COLUMN update_time TYPE timestamp"
                " with time zone USING update_time::timestamp with time zone;"
            ),
            "ALTER TABLE word_bank2 RENAME COLUMN user_qq TO user_id;",
            # 将user_qq改为user_id
            "ALTER TABLE word_bank2 ALTER COLUMN user_id TYPE character varying(255);",
            "ALTER TABLE word_bank2 ALTER COLUMN group_id TYPE character varying(255);",
            "ALTER TABLE word_bank2 ADD platform varchar(255) DEFAULT 'qq';",
            "ALTER TABLE word_bank2 ADD author varchar(255) DEFAULT '';",
        ]
