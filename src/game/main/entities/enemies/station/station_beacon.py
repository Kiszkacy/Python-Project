from typing import List

import arcade

from src.game.main.entities.structure import Structure
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.interfaces.collidable import Collidable


class EnemyStationBeacon(Structure):

    def __init__(self, sprite_url: str, hp_max: float, shd_max: float, station: Structure, starting_orbit_angle: float, starting_orbit_speed: float, orbit_radius: float) -> None:
        super(EnemyStationBeacon, self).__init__(sprite_url=sprite_url,
                                           mass=1000.0, belongs_to=ObjectCategory.ENEMIES,
                                           collides_with=[ObjectCategory.STATIC, ObjectCategory.PLAYER, ObjectCategory.PROJECTILES, ObjectCategory.ENEMIES],
                                           hp_max=hp_max, shd_max=shd_max, power_max=1000.0)
        self.invulnerable: bool = True
        self.station: Structure = station
        self.orbit_angle: float = starting_orbit_angle # in degrees
        self.orbit_speed: float = starting_orbit_speed # in degrees
        self.orbit_radius: float = orbit_radius # in pixels

    def handle_collisions(self, delta: float) -> List[Collidable]:
        return []  # remove collisions so the object is immovable

    def on_update(self, delta_time: float = 1 / 60) -> None:
        super(EnemyStationBeacon, self).on_update(delta_time)
        # move
        self.orbit_angle += self.orbit_speed
        rotated: List[float] = arcade.rotate_point(self.orbit_radius+self.station.position[0], 0+self.station.position[1],
                                                   self.station.position[0], self.station.position[1], self.orbit_angle)
        self.position = (rotated[0], rotated[1])


if __name__ == '__main__':
    pass
