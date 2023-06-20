from typing import Tuple, List

import arcade

from src.game.main.entities.enemies.station.shield_beacon import EnemyStationBeacon, EnemyStationShieldBeacon
from src.game.main.entities.enemies.station.station import EnemyStation
from src.game.main.entities.entity import Entity
from src.game.main.entities.formations.formation import Formation
from src.game.main.entities.friendly.weapon_station import WeaponStation
from src.game.main.util.rand import randrange


class TradeStation(Formation):

    def __init__(self) -> None:
        super(TradeStation, self).__init__(width=200, height=200, entities=[(WeaponStation(), (0,0))])


if __name__ == '__main__':
    pass
