from typing import List, Optional
from enum import IntEnum
from dataclasses import dataclass
from datetime import datetime, timedelta


class NoMoreEvents(Exception):
    """Raised when the scheduler have no more events scheduled"""


class EventTypesEnum(IntEnum):
    """Defines what the different event can be"""

    DEPARTURE = 0
    ARRIVAL = 1


@dataclass
class Event:
    """Defines what a event is"""

    type_: EventTypesEnum  # type of the event
    time: datetime  # time of the event

    def __str__(self) -> str:
        return f"{self.type_.name}, {self.time}"


class EventScheduler:
    """Holds the next event to occurs"""

    def __init__(self):
        self._events: List[Event] = []

    def add(self, type_: EventTypesEnum, delay: float):
        now = datetime.now()

        evt = Event(
            type_=type_,
            time=now + timedelta(seconds=delay),
        )

        self._events.append(evt)

    def get_next(self) -> Optional[Event]:

        if not self._events:
            raise NoMoreEvents()

        now = datetime.now()

        for e in self._events:
            if e.time <= now:
                self._events.remove(e)
                return e
