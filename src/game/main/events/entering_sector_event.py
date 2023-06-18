from __future__ import annotations
from dataclasses import dataclass

from src.game.main.events.event import Event
from src.game.main.sectors.sector_master import Node


@dataclass
class SectorCompleted(Event):
    pass


if __name__ == '__main__':
    pass
