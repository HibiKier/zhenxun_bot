from typing import List
from .Talent import Talent

class WeightedEvent:
    def __init__(self, o: str):
        if '*' not in o:
            self.weight: float = 1.0
            self.evt: int = int(o)
        else:
            s = o.split('*')
            self.weight: float = float(s[1])
            self.evt: int = int(s[0])

class AgeManager:
    @staticmethod
    def load(config):
        AgeManager._ages = config
        for a in AgeManager._ages:
            if 'event' in AgeManager._ages[a]:
                AgeManager._ages[a]['event'] = [WeightedEvent(str(x)) for x in AgeManager._ages[a]['event']]

    def __init__(self, base):
        self._base = base

    def _getnow(self):
        return AgeManager._ages[str(self._base.property.AGE)]
    
    def getEvents(self) -> List[WeightedEvent]:
        now = self._getnow()
        if 'event' in now: return now['event']
        return []
    
    def getTalents(self) -> List[Talent]:
        now = self._getnow()
        if 'talent' in now: return now['talent']
        return []
    
    def grow(self):
        self._base.property.AGE += 1