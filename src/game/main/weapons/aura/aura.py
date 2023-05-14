
from src.game.main.entities.projectile import Projectile
from src.game.main.util.path_loader import get_absolute_resource_path
from src.game.main.weapons.launchable_gun import LaunchableGun
from src.game.main.weapons.weapon import Weapon


class ProjectileAura(Projectile):

    def __init__(self) -> None:
        Projectile.__init__(self, sprite_url=get_absolute_resource_path("\\sprites\\projectiles\\small_001.png"),
                            acceleration=350.0,
                            lifetime=1.8)


class GunAura(LaunchableGun):

    def __init__(self) -> None:
        super().__init__(launchable=ProjectileAura(),
                         barrel_count=16,
                         even_spread=360.0,
                         launch_spread=0.0,
                         launch_speed=100.0,
                         shot_spread=25.0,
                         power_cost=1.0)


class WeaponAura(Weapon):

    def __init__(self) -> None:
        super(WeaponAura, self).__init__(GunAura())


if __name__ == '__main__':
    pass
