
from src.game.main.entities.projectile import Projectile
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.util.path_loader import get_absolute_resource_path
from src.game.main.weapons.launchable_gun import LaunchableGun
from src.game.main.weapons.weapon import Weapon


class ProjectileQuick(Projectile):

    def __init__(self) -> None:
        Projectile.__init__(self, sprite_url=get_absolute_resource_path("\\sprites\\projectiles\\small_005.png"),
                            collides_with=[ObjectCategory.PLAYER, ObjectCategory.NEUTRAL, ObjectCategory.STATIC],
                            damage=2, lifetime=1.5)


class GunQuick(LaunchableGun):

    def __init__(self) -> None:
        super().__init__(launchable=ProjectileQuick(), launch_speed=650.0, shots_per_sec=3.5, barrels_even_offset=24.0, barrel_count=2)


class WeaponQuick(Weapon):

    def __init__(self) -> None:
        super(WeaponQuick, self).__init__(GunQuick())


if __name__ == '__main__':
    pass
