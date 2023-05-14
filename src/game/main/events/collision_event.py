from dataclasses import dataclass

import arcade

from src.game.main.events.event import Event
from src.game.main.interfaces.collidable import Collidable


@dataclass
class CollisionEvent(Event):
    collided: Collidable
    with_: Collidable
    at: arcade.Point


if __name__ == '__main__':
    pass
