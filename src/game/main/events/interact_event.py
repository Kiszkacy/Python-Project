from dataclasses import dataclass

import arcade

from src.game.main.entities.player_ship import PlayerShip
from src.game.main.events.event import Event


@dataclass
class InteractEvent(Event):
    player: PlayerShip
    at: arcade.Point


if __name__ == '__main__':
    pass
