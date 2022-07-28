from .AgeManager import WeightedEvent
from typing import Dict, Iterator, List, Set
from .Event import Event

class EventManager:

    @staticmethod
    def load(config):
        EventManager._events: Dict[int, Event] = dict((int(k), Event(config[k]))for k in config)
        for k in EventManager._events:
            for b in EventManager._events[k].branch:
                b.evt = EventManager._events[b.id]

    def __init__(self, base, rnd):
        self._base = base
        self.triggered: Set[int] = set()
        self._rnd = rnd

    def _randEvent(self, events: List[WeightedEvent]) -> int:
        events_checked = [ev for ev in events if EventManager._events[ev.evt].checkCondition(self._base.property)]
        total = sum(e.weight for e in events_checked)
        rnd = self._rnd.random() * total
        for ev in events_checked:
            rnd -= ev.weight
            if rnd <= 0: return ev.evt
        return events[0].evt
    
    def _runEvent(self, event: Event) -> Iterator[str]:
        self.triggered.add(event.id)
        return event.runEvent(self._base.property, self._runEvent)

    def runEvents(self, events: List[WeightedEvent]) -> Iterator[str]:
        ev = self._randEvent(events)
        return self._runEvent(EventManager._events[ev])