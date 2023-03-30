
import arcade
from src.entities.projectiles.Projectile import Projectile
from src.interfaces.Launchable import Launchable
from src.singletons.EntityHandler import EntityHandler
from src.weapons.Gun import Gun
from copy import deepcopy
import numpy as np


class LaunchableGun(Gun):

    def __init__(self, damage: float = 3.0, power_cost: float = 2.0, barrel_count: int = 1,
                 barrels: list[arcade.Point] = None, barrels_even_offset: float = 3.0, launch_speed: float = 500.0,
                 launch_spread: float = 0.0, shot_spread: float = 5.0, even_spread: float = 0.0,
                 shots_per_sec: float = 5.0, launchable: Launchable = Projectile("..\\resources\\sprites\\tmp_projectile.png")) -> None:
        # TODO change path to error texture
        super().__init__(damage, power_cost, barrel_count, barrels, barrels_even_offset)
        # launchableGun stats
        self.launch_speed: float = launch_speed
        self.launch_spread: float = launch_spread
        self.shot_spread: float = shot_spread
        self.even_spread: float = even_spread # TODO currently not working -> add with custom spread angles
        self.shots_per_sec: float = shots_per_sec
        self.launchable: Launchable = launchable
        # TODO add more: penetrations, bounces, explosions, lifetime, falloff damage, projectile variety, custom spread angles etc


    def shoot(self, from_: arcade.Point, angle: float) -> None:
        shot_angle: float = angle + np.random.uniform(-0.5, 0.5)*self.shot_spread
        pos_offset: arcade.Vector = (-np.sin(np.rad2deg(angle)), np.cos(np.rad2deg(angle)))
        for i in range(self.barrel_count):
            launch_angle: float = shot_angle + np.random.uniform(-0.5, 0.5)*self.launch_spread
            launch_pos: arcade.Vector = (from_[0] + pos_offset[0]*self.barrels[i][0], from_[1] + pos_offset[1]*self.barrels[i][1])
            instance: Launchable = deepcopy(self.launchable)
            # TODO report this instance to a proper singleton
            instance.launch(launch_pos, launch_angle, self.launch_speed)
            EntityHandler.everything.append(instance) # TODO redo when entityHandler is done
        # set cooldown
        self.cd = 1.0 / self.shots_per_sec





if __name__ == '__main__':
    pass
