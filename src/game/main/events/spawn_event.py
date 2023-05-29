from dataclasses import dataclass

import arcade

from src.game.main.entities.entity import Entity
from src.game.main.events.event import Event


@dataclass
class SpawnEvent(Event):
    spawned: Entity
    at: arcade.Point


if __name__ == '__main__':
    pass
