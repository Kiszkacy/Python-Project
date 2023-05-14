from __future__ import annotations
from dataclasses import dataclass

from src.game.main.entities.entity import Entity
from src.game.main.events.event import Event
import src.game.main.interfaces.damageable as _


@dataclass
class DamageEvent(Event):
    damaged: _.Damageable
    amount: float
    by: Entity


if __name__ == '__main__':
    pass
