
from collections import deque
from typing import List

from src.game.main.events.event import Event
from src.game.main.events.event_observer import Observer
from src.game.main.singletons.config import Config
from src.game.main.singletons.singleton import Singleton


class EventRegister(metaclass=Singleton):

    recent_events: deque[Event] = deque(maxlen=Config.Constants.get("EVENT_REGISTER_SIZE"))
    observers: List[Observer] = []

    @staticmethod
    def register_new(event: Event) -> None:
        EventRegister.recent_events.append(event)
        EventRegister.notify(event)

    @staticmethod
    def notify(about: Event) -> None:
        for observer in EventRegister.observers:

            observer.notify(about)

    @staticmethod
    def add_observer(observer: Observer) -> bool:
        EventRegister.observers.append(observer) # TODO check if not a duplicate
        return True


if __name__ == '__main__':
    pass
