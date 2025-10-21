from __future__ import annotations

import threading, time
from dataclasses import dataclass
from typing import Callable, Dict, List, Any

@dataclass
class Event:
    type: str
    owner: str
    ts: int
    data: Dict[str, Any]

Subscriber = Callable[[Event], None]

class EventBus:
    def __init__(self):
        self._subs: List[Subscriber] = []
        self._lock = threading.Lock()
    def subscribe(self, fn: Subscriber):
        with self._lock:
            self._subs.append(fn)
        return fn
    def publish(self, evt: Event):
        with self._lock:
            subs = list(self._subs)
        for fn in subs:
            try:
                fn(evt)
            except Exception:
                pass

BUS = EventBus()

def now() -> int:
    return int(time.time())

def emit(evt_type: str, owner: str, **data):
    BUS.publish(Event(type=evt_type, owner=owner, ts=now(), data=data))
