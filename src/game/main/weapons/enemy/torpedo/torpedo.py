
from src.game.main.entities.projectile import Projectile
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.util.path_loader import get_absolute_resource_path
from src.game.main.weapons.launchable_gun import LaunchableGun
from src.game.main.weapons.weapon import Weapon


class ProjectileTorpedo(Projectile):

    def __init__(self) -> None:
        Projectile.__init__(self, sprite_url=get_absolute_resource_path("\\sprites\\projectiles\\big_004.png"),
                            collides_with=[ObjectCategory.PLAYER, ObjectCategory.NEUTRAL, ObjectCategory.STATIC],
                            damage=15, lifetime=1.5, acceleration=750.0)


class GunTorpedo(LaunchableGun):

    def __init__(self) -> None:
        super().__init__(launchable=ProjectileTorpedo(), launch_speed=100.0, shots_per_sec=0.4)


class WeaponTorpedo(Weapon):

    def __init__(self) -> None:
        super(WeaponTorpedo, self).__init__(GunTorpedo())


if __name__ == '__main__':
    pass
