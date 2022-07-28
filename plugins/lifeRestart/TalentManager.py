from typing import Dict, List, Set, Iterator
from .Talent import Talent

class TalentManager:
    grade_count = 4
    grade_prob = [0.889, 0.1, 0.01, 0.001]

    @staticmethod
    def load(config):
        TalentManager._talents: Dict[int, List[Talent]] = dict([(i, []) for i in range(TalentManager.grade_count)])
        TalentManager.talentDict: Dict[int, Talent] = dict()
        
        for k in config.keys():
            t = Talent(config[k])
            TalentManager._talents[t.grade].append(t)
            TalentManager.talentDict[t.id] = t

    def __init__(self, base, rnd):
        self._base = base
        self.talents: List[Talent] = []
        self.triggered: Set[int] = set()
        self._rnd = rnd

    def _genGrades(self):
        rnd = self._rnd.random()
        result = TalentManager.grade_count
        while rnd > 0:
            result -= 1
            rnd -= TalentManager.grade_prob[result]
        return result
    
    def genTalents(self, count: int) -> Iterator[Talent]:
        # should not repeats
        counts = dict([(i, 0) for i in range(TalentManager.grade_count)])
        for _ in range(count):
            counts[self._genGrades()] += 1
        for grade in range(TalentManager.grade_count - 1, -1, -1):
            count = counts[grade]
            n = len(TalentManager._talents[grade])
            if count > n:
                counts[grade - 1] += count - n
                count = n
            for talent in self._rnd.sample(TalentManager._talents[grade], k=count):
                yield talent

    def updateTalentProp(self):
        self._base.property.total += sum(t.status for t in self.talents)

    def updateTalent(self) -> Iterator[str]:
        for t in self.talents:
            if t.id in self.triggered: continue
            for res in t.runTalent(self._base.property):
                self.triggered.add(t.id)
                yield res

    def addTalent(self, talent: Talent):
        for t in self.talents:
            if t.id == talent.id: return
        self.talents.append(talent)