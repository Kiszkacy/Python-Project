from typing import Tuple, List

import arcade

from src.game.main.entities.enemies.station.shield_beacon import EnemyStationBeacon, EnemyStationShieldBeacon
from src.game.main.entities.enemies.station.station import EnemyStation
from src.game.main.entities.entity import Entity
from src.game.main.entities.formations.formation import Formation
from src.game.main.util.rand import randrange


class RivalStation(Formation):

    def __init__(self) -> None:
        beacon_count: int = 4+randrange(0,1)*2 # 4 or 6
        orbit_radius: float = randrange(4,5)*75.0
        entities: List[Tuple[Entity, arcade.Point]] = []

        station: EnemyStation = EnemyStation()
        entities.append((station, (0,0)))
        for i in range(beacon_count):
            beacon: EnemyStationBeacon = EnemyStationShieldBeacon(station,
                                                            starting_orbit_angle=i*(360.0/beacon_count),
                                                            starting_orbit_speed=0.1,
                                                            orbit_radius=orbit_radius) # if i % 2 == 0 else EnemyStationTurretBeacon(station,
                                                            # starting_orbit_angle=i*(360.0/beacon_count),
                                                            # starting_orbit_speed=0.1,
                                                            # orbit_radius=orbit_radius)

            station.beacons.append(beacon)
            entities.append((beacon, (0,0)))

        super(RivalStation, self).__init__(width=960, height=960, entities=entities)


if __name__ == '__main__':
    pass
