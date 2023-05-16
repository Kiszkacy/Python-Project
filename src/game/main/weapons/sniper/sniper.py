
from src.game.main.entities.projectile import Projectile
from src.game.main.tempclasses.temp_enemy import TempEnemy
from src.game.main.util.path_loader import get_absolute_resource_path
from src.game.main.weapons.launchable_gun import LaunchableGun
from src.game.main.weapons.weapon import Weapon


class ProjectileSniper(Projectile):

    def __init__(self) -> None:
        Projectile.__init__(self, sprite_url=get_absolute_resource_path("\\sprites\\projectiles\\big_002.png"),
                            damage=25.0, lifetime=1.5)


class GunSniper(LaunchableGun):

    def __init__(self) -> None:
        super().__init__(launchable=ProjectileSniper(), launch_speed=900.0, shots_per_sec=1.5, shot_spread=0.0, launch_spread=0.0)


class WeaponSniper(Weapon):

    def __init__(self) -> None:
        super(WeaponSniper, self).__init__(GunSniper())


if __name__ == '__main__':
    pass
