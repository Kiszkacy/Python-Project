
from src.game.main.entities.projectile import Projectile
from src.game.main.tempclasses.temp_enemy import TempEnemy
from src.game.main.util.path_loader import get_absolute_resource_path
from src.game.main.weapons.launchable_gun import LaunchableGun
from src.game.main.weapons.weapon import Weapon


class ProjectileBasic(Projectile):

    def __init__(self) -> None:
        Projectile.__init__(self, sprite_url=get_absolute_resource_path("\\sprites\\projectiles\\small_003.png"))


class GunBasic(LaunchableGun):

    def __init__(self) -> None:
        super().__init__(launchable=ProjectileBasic())


class GunBasicAlt(LaunchableGun):

    def __init__(self) -> None:
        super().__init__(launchable=TempEnemy(),
                         launch_speed=200.0,
                         shots_per_sec=3.0,
                         power_cost=7.0)


class WeaponBasic(Weapon):

    def __init__(self) -> None:
        super(WeaponBasic, self).__init__(GunBasic(), GunBasicAlt())


if __name__ == '__main__':
    pass
