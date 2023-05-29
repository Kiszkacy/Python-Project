
from src.game.main.entities.enemies.station.station_beacon import EnemyStationBeacon
from src.game.main.entities.structure import Structure
from src.game.main.util.path_loader import get_absolute_resource_path


class EnemyStationShieldBeacon(EnemyStationBeacon):

    def __init__(self, station: Structure, starting_orbit_angle: float, starting_orbit_speed: float, orbit_radius: float) -> None:
        super(EnemyStationShieldBeacon, self).__init__(get_absolute_resource_path("\\sprites\\stationary\\station_beacon_001.png"),
                                           50.0, 50.0, station, starting_orbit_angle, starting_orbit_speed, orbit_radius)


if __name__ == '__main__':
    pass
