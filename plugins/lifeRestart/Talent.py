from typing import Dict, List
from .Utils import parseCondition

class Talent:
    def __init__(self, json):
        self.id: int = int(json['id'])
        self.name: str = json['name']
        self.desc: str = json['description']
        self.grade: int = int(json['grade'])
        self._exclusive: List[int] = [int(x) for x in json['exclusive']] if'exclusive' in json else []
        self._effect: Dict[str, int] = json['effect'] if 'effect' in json else {}
        self.status = int(json['status']) if 'status' in json else 0
        self._cond = parseCondition(json['condition']) if 'condition' in json else lambda _: True
    def isExclusiveWith(self, talent) -> bool:
        return talent.id in self._exclusive or self.id in talent._exclusive
    def __str__(self) -> str:
        return f'Talent(name={self.name}, desc={self.desc})'
    def _checkCondition(self, prop) -> bool:
        return self._cond(prop)
    def runTalent(self, prop) -> List[str]:
        if self._checkCondition(prop):
            prop.apply(self._effect)
            return [f'天赋【{self.name}】发动：{self.desc}']
        return []