
from dataclasses import dataclass

from src.game.main.events.event import Event
from src.game.main.interfaces.destroyable import Destroyable


@dataclass
class DestroyEvent(Event):
    destroyed: Destroyable


if __name__ == '__main__':
    pass
