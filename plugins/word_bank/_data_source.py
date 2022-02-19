from .model import WordBank
from typing import Union


class WordBankBuilder:

    def __init__(self, user_id: int, group_id: int, problem: str):

        self._data = {
            "user_id": user_id,
            "group_id": group_id,
            "problem": problem
        }

    def set_placeholder(self, id_: int, placeholder: Union[str, int]):
        """
        设置占位符
        :param id_: 站位id
        :param placeholder: 占位符内容
        """
        if self._data.get("placeholder") is None:
            self._data["placeholder"] = []
        self._data["placeholder"].append((id_, placeholder))

    def set_answer(self, answer: str):
        """
        设置回答
        :param answer: 回答
        """
        self._data["answer"] = answer

    async def save(self):
        user_id = self._data["user_id"]
        group_id = self._data["group_id"]
        problem = self._data["problem"]
        answer = self._data["answer"]
        placeholder = self._data.get("placeholder")
        await WordBank.add_problem_answer(user_id, group_id, problem, answer, placeholder)

    def __str__(self):
        return str(self._data)











