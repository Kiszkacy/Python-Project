import copy

import numpy as np

from src.game.main.entities.projectile import Projectile
from src.game.main.movement.sinusoidal_movement import SinusoidalMovement
from src.game.main.util.path_loader import get_absolute_resource_path
from src.game.main.weapons.launchable_gun import LaunchableGun
from src.game.main.weapons.weapon import Weapon


class GunSinus(LaunchableGun):

    def __init__(self) -> None:
        super().__init__(launchable=ProjectileSinus(), shot_spread=0.0, launch_spread=0.0, shots_per_sec=8.0)


class ProjectileSinus(Projectile):

    def __init__(self) -> None:
        Projectile.__init__(self, sprite_url=get_absolute_resource_path("\\sprites\\tmp_projectile0.png"),
                            movement_type=SinusoidalMovement(16.0, 96.0, 800.0, np.random.uniform()*np.pi*2))

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))

        result.movement_type.time = np.random.uniform()*np.pi*2
        return result


class WeaponSinus(Weapon):

    def __init__(self) -> None:
        super(WeaponSinus, self).__init__(GunSinus())


if __name__ == '__main__':
    pass
