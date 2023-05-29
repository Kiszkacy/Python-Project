import arcade
import numpy as np

from src.game.main.entities.enemies.station.station_beacon import EnemyStationBeacon

from src.game.main.entities.structure import Structure
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.interfaces.destroyable import Destroyable
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.util.path_loader import get_absolute_resource_path


class EnemyStationTurretBeacon(EnemyStationBeacon):

    def __init__(self, station: Structure, starting_orbit_angle: float, starting_orbit_speed: float, orbit_radius: float) -> None:
        super(EnemyStationTurretBeacon, self).__init__(get_absolute_resource_path("\\sprites\\stationary\\station_beacon_002.png"),
                                           25.0, 50.0, station, starting_orbit_angle, starting_orbit_speed, orbit_radius)
        self.turret_sprite: arcade.Sprite = arcade.Sprite(get_absolute_resource_path("\\sprites\\stationary\\station_turret.png"))
        EntityHandler.add(self.turret_sprite, ObjectCategory.MISC, False)

    def on_update(self, delta_time: float = 1 / 60) -> None:
        super(EnemyStationTurretBeacon, self).on_update(delta_time)
        self.turret_sprite.position = self.position
        # rotate turret here and shoot if ...
        # TODO tmp code
        x_diff: float = EntityHandler.player.position[0] - self.position[0]
        y_diff: float = EntityHandler.player.position[1] - self.position[1]
        target_angle_rad: float = np.arctan2(y_diff, x_diff)
        self.rotate_towards(delta_time, target_angle_rad)
        # self.turret_sprite.on_update(delta_time)

    # TODO CODE REPETITION
    def rotate_towards(self, delta: float, target_angle_radians: float) -> None:
        target_angle_rad: float = target_angle_radians

        if target_angle_rad < 0.0: target_angle_rad += 2 * np.pi
        angle_rad: float = np.deg2rad(self.turret_sprite.angle)
        rotation_rad: float = np.deg2rad(40.0) # rotation speed
        angle_rad_diff: float = target_angle_rad - angle_rad
        # rotation clockwise or anticlockwise?
        clockwise: bool = False
        if abs(angle_rad_diff) <= rotation_rad * delta:
            # jump to target angle if small
            angle_rad = target_angle_rad
        elif angle_rad_diff > 0 and abs(angle_rad_diff) >= np.pi:
            clockwise = True
        elif angle_rad_diff < 0 and abs(angle_rad_diff) < np.pi:
            clockwise = True

        if angle_rad != target_angle_rad and clockwise:
            angle_rad -= rotation_rad * delta
        elif angle_rad != target_angle_rad:
            angle_rad += rotation_rad * delta

        if angle_rad > 2 * np.pi:
            angle_rad -= 2 * np.pi
        elif angle_rad < 0:
            angle_rad += 2 * np.pi

        self.turret_sprite.angle = np.degrees(angle_rad)


    def destroy(self) -> Destroyable:
        self.turret_sprite.kill()
        return super(EnemyStationTurretBeacon, self).destroy()


if __name__ == '__main__':
    pass
