
from src.game.main.entities.projectile import Projectile
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.util.path_loader import get_absolute_resource_path
from src.game.main.weapons.launchable_gun import LaunchableGun
from src.game.main.weapons.weapon import Weapon


class ProjectileBasic(Projectile):

    def __init__(self) -> None:
        Projectile.__init__(self, sprite_url=get_absolute_resource_path("\\sprites\\projectiles\\small_006.png"),
                            collides_with=[ObjectCategory.PLAYER, ObjectCategory.NEUTRAL, ObjectCategory.STATIC],
                            damage=3)


class GunBasic(LaunchableGun):

    def __init__(self) -> None:
        super().__init__(launchable=ProjectileBasic(), launch_speed=600.0, shots_per_sec=2.0)


class WeaponBasic(Weapon):

    def __init__(self) -> None:
        super(WeaponBasic, self).__init__(GunBasic())


if __name__ == '__main__':
    pass
