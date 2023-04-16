
from src.game.main.entities.projectile import Projectile
from src.game.main.util.path_loader import get_absolute_resource_path
from src.game.main.weapons.launchable_gun import LaunchableGun
from src.game.main.weapons.weapon import Weapon


class GunWeird(LaunchableGun):

    def __init__(self) -> None:
        super().__init__(launchable=ProjectileWeird(),
                         shot_spread=0.0,
                         launch_spread=10.0,
                         barrel_count=6,
                         custom_spread=[-45.0, -30.0, 0.0, 30.0, 45.0, -180.0],
                         shots_per_sec=6.0,
                         launch_speed=600.0)


class ProjectileWeird(Projectile):

    def __init__(self) -> None:
        Projectile.__init__(self, sprite_url=get_absolute_resource_path("\\sprites\\tmp_projectile2.png"),
                            acceleration=-150.0)


class WeaponWeird(Weapon):

    def __init__(self) -> None:
        super(WeaponWeird, self).__init__(GunWeird())


if __name__ == '__main__':
    pass
