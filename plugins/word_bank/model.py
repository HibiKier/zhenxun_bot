from services.db_context import db
from typing import Optional, List, Union, Tuple
from datetime import datetime
from pathlib import Path
from configs.path_config import DATA_PATH
import re
import random


class WordBank(db.Model):
    __tablename__ = "word_bank"

    user_qq = db.Column(db.BigInteger(), nullable=False)
    group_id = db.Column(db.Integer())
    search_type = db.Column(db.Integer(), nullable=False, default=0)
    problem = db.Column(db.String(), nullable=False)
    answer = db.Column(db.String(), nullable=False)
    format = db.Column(db.String())
    create_time = db.Column(db.DateTime(), nullable=False)
    update_time = db.Column(db.DateTime(), nullable=False)

    @classmethod
    async def add_problem_answer(
        cls,
        user_id: int,
        group_id: Optional[int],
        problem: str,
        answer: str,
        format_: Optional[List[Tuple[int, Union[int, str]]]],
    ) -> bool:
        """
        添加或新增一个问答
        :param user_id: 用户id
        :param group_id: 群号
        :param problem: 问题
        :param answer: 回答
        :param format_: 格式化数据
        """
        _str = None
        if format_:
            _str = ""
            for x, y in format_:
                _str += f"{x}<_s>{y}<format>"
        return await cls._problem_answer_handle(
            user_id, group_id, problem, "add", answer=answer, format_=_str
        )

    @classmethod
    async def delete_problem_answer(
        cls, user_id: int, group_id: Optional[int], problem: str, index: Optional[int]
    ) -> str:
        """
        删除某问题一个或全部回答
        :param user_id: 用户id
        :param group_id: 群号
        :param problem: 问题
        :param index: 回答下标
        """
        return await cls._problem_answer_handle(
            user_id, group_id, problem, "delete", index=index
        )

    @classmethod
    async def get_problem_answer(
        cls, user_id: int, group_id: Optional[int], problem: str
    ) -> List[str]:
        """
        获取问题的所有回答
        :param user_id: 用户id
        :param group_id: 群号
        :param problem: 问题
        """
        return await cls._problem_answer_handle(user_id, group_id, problem, "get")

    @classmethod
    async def get_group_all_answer(cls, group_id: int, problem: str) -> List[str]:
        """
        获取群聊指定词条所有回答
        :param group_id: 群号
        :param problem: 问题
        """
        if problem.startswith("id:"):
            problem_index = int(problem.split(":")[-1])
            q = await cls.get_group_all_problem(group_id)
            if len(q) > problem_index:
                problem = q[problem_index]
        q = await cls.query.where(
            (cls.group_id == group_id) & (cls.problem == problem)
        ).gino.all()
        return [x.answer for x in q] if q else None

    @classmethod
    async def get_group_all_problem(cls, group_id: int) -> List[str]:
        """
        获取群聊所有词条
        :param group_id: 群号
        """
        q = await cls.query.where(cls.group_id == group_id).gino.all()
        q = [x.problem for x in q]
        q.sort()
        _tmp = []
        for problem in q:
            if "[_to_me" in problem:
                r = re.search(r"\[_to_me\|(.*?)](.*)", problem)
                if r:
                    bot_name = r.group(1)
                    problem = problem.replace(f"[_to_me|{bot_name}]", bot_name)
            _tmp.append(problem)
        return list(set(_tmp))

    @classmethod
    async def check(cls, group_id: int, problem: str, is_tome: bool = False) -> Optional["WordBank"]:
        """
        检测词条并随机返回
        :param group_id: 群号
        :param problem: 问题
        :param is_tome：是否at真寻
        """
        if is_tome:
            q = await cls.query.where(
                (cls.group_id == group_id)
            ).gino.all()
            q = [x for x in q if "[_to_me" in x.problem]
            if q:
                for x in q:
                    r = re.search(r"\[_to_me\|(.*?)](.*)", x.problem)
                    if r and r.group(2) == problem:
                        return x
            return None
        else:
            q = await cls.query.where(
                (cls.group_id == group_id) & (cls.problem == problem)
            ).gino.all()
        return random.choice(q) if q else None

    @classmethod
    async def _problem_answer_handle(
        cls,
        user_id: int,
        group_id: Optional[int],
        problem: str,
        type_: str,
        *,
        answer: Optional[str] = None,
        index: Optional[int] = None,
        format_: Optional[str] = None,
    ) -> Union[List[Union[str, Tuple[str, str]]], bool, str]:
        """
        添加或新增一个问答
        :param user_id: 用户id
        :param group_id: 群号
        :param problem: 问题
        :param type_: 操作类型
        :param answer: 回答
        :param format_: 格式化数据
        """
        if problem.startswith("id:"):
            problem_index = int(problem.split(":")[-1])
            q = await cls.get_group_all_problem(group_id)
            if not q:
                return []
            if len(q) > problem_index:
                problem = q[problem_index]
        if group_id:
            q = cls.query.where((cls.group_id == group_id) & (cls.problem == problem))
        else:
            q = cls.query.where((cls.user_qq == user_id) & (cls.problem == problem))
        if type_ == "add":
            q = await q.where(cls.answer == answer).gino.all()
            if not q or ".jpg" in format_:
                await cls.create(
                    user_qq=user_id,
                    group_id=group_id,
                    problem=problem,
                    answer=answer,
                    format=format_,
                    create_time=datetime.now().date(),
                    update_time=datetime.now().date(),
                )
            return True
        elif type_ == "delete":
            q = await q.with_for_update().gino.all()
            if q:
                path = DATA_PATH / "word_bank" / f"{group_id}"
                if index is not None:
                    _q = [x.problem for x in q]
                    _q.sort()
                    prob = _q[index]
                    index = [x.problem for x in q].index(prob)
                    q = [q[index]]
                answer = "\n".join([x.answer for x in q])
                for x in q:
                    format_ = x.format
                    if format_:
                        for sp in format_.split("<format>")[:-1]:
                            _, image_name = sp.split("<_s>")
                            if image_name.endswith("jpg"):
                                _path = path / image_name
                                if _path.exists():
                                    _path.unlink()
                    await cls.delete.where(
                        (cls.problem == problem)
                        & (cls.answer == x.answer)
                        & (cls.group_id == group_id)
                    ).gino.status()
                return answer
        elif type_ == "get":
            q = await q.gino.all()
            if q:
                return [(x.answer, x.format.split("<format>")[:-1]) for x in q]
        return False

