
import arcade

from src.entities.Entity import Entity
from src.entities.Projectile import Projectile
from src.interfaces.Launchable import Launchable
from src.singletons.EntityHandler import EntityHandler
from src.auxilary.ObjectCategory import ObjectCategory
from src.weapons.Gun import Gun
from copy import deepcopy
import numpy as np


class LaunchableGun(Gun):

    def __init__(self, power_cost: float = 2.0, barrel_count: int = 1,
                 barrels: list[arcade.Point] = None, barrels_even_offset: float = 3.0, launch_speed: float = 800.0,
                 launch_spread: float = 0.0, shot_spread: float = 5.0, even_spread: float = 0.0, custom_spread: list[float] = None,
                 shots_per_sec: float = 5.0,
                 launchable: Launchable = Projectile("..\\resources\\sprites\\tmp_projectile0.png",
                                                     ObjectCategory.PROJECTILES, [ObjectCategory.ENEMIES])) -> None:
        # TODO change path to error texture
        super().__init__(power_cost, barrel_count, barrels, barrels_even_offset)
        # launchableGun stats
        self.launch_speed: float = launch_speed
        self.launch_spread: float = launch_spread
        self.shot_spread: float = shot_spread
        self.even_spread: float = even_spread
        self.shots_per_sec: float = shots_per_sec
        self.launchable: Launchable = launchable
        # SCRIPT VARS "PRIVATE"
        self.spread_angles: list[float] = [0.0 for _ in range(barrel_count)] if custom_spread is None else custom_spread
        if barrel_count == 1: return # TODO custom and/or even spread angles are calculated at init so they cannot be changed midgame
        for i in range(barrel_count):
            self.spread_angles[i] += -even_spread/2 + i * (even_spread/(barrel_count-1))


    def shoot(self, from_: arcade.Point, angle: float) -> None:
        shot_angle: float = angle + np.random.uniform(-0.5, 0.5)*self.shot_spread # get shot spread
        pos_offset: arcade.Vector = (-np.sin(np.rad2deg(angle)), np.cos(np.rad2deg(angle))) # get correct position
        for i in range(self.barrel_count): # shoot how many barrels you have
            self.launch(from_, shot_angle, pos_offset, i)
        # set cooldown
        self.cd = 1.0 / self.shots_per_sec


    def launch(self, from_: arcade.Point, angle: float, pos_offset: arcade.Vector, idx: int) -> None:
        launch_angle: float = angle + np.random.uniform(-0.5, 0.5) * self.launch_spread + self.spread_angles[idx]
        launch_pos: arcade.Vector = (from_[0] + pos_offset[0] * self.barrels[idx][0], from_[1] + pos_offset[1] * self.barrels[idx][1])
        instance: Launchable and Entity = deepcopy(self.launchable)
        instance.launch(launch_pos, launch_angle, self.launch_speed)
        EntityHandler.add(instance, instance.belongs_to)


if __name__ == '__main__':
    pass
