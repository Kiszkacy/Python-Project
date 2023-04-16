
import arcade
from src.game.main.entities.projectile import Projectile
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.interfaces.launchable import Launchable
from src.game.main.util.path_loader import get_absolute_resource_path
from src.game.main.weapons.launchable_gun import LaunchableGun
from src.game.main.weapons.weapon import Weapon


class GunShotgun(LaunchableGun):

    def __init__(self) -> None:
        self.launchables: list[Launchable] = [ProjectileShotgunSmall(), ProjectileShotgunBig()]
        self.launchable_idx: int = 0
        super().__init__(
            power_cost=7.0,
            barrel_count=7,
            barrels_even_offset=25.0,
            launch_speed=700.0,
            launch_spread=5.0,
            shot_spread=10.0,
            even_spread=35.0,
            shots_per_sec=2.0,
            launchable=self.launchables[self.launchable_idx])

    def launch(self, from_: arcade.Point, angle: float, idx: int) -> None:
        super(GunShotgun, self).launch(from_, angle, idx)
        self.launchable_idx = (self.launchable_idx+1) % len(self.launchables)
        self.launchable = self.launchables[self.launchable_idx]


class GunShotgunAlt(LaunchableGun):

    def __init__(self) -> None:
        super().__init__(
            power_cost=4.0,
            barrel_count=3,
            barrels_even_offset=45.0,
            launch_speed=700.0,
            launch_spread=1.0,
            shot_spread=5.0,
            even_spread=12.0,
            shots_per_sec=4.0,
            launchable=ProjectileShotgunAlt())


class ProjectileShotgunAlt(Projectile):

    def __init__(self) -> None:
        Projectile.__init__(self, sprite_url=get_absolute_resource_path("\\sprites\\tmp_projectile2.png"),
                            damage=12.0,
                            acceleration=-400.0,
                            lifetime=3.0)


class ProjectileShotgunBig(Projectile):

    def __init__(self) -> None:
        Projectile.__init__(self, sprite_url=get_absolute_resource_path("\\sprites\\tmp_projectile1.png"),
                            damage=15.0,
                            acceleration=-300.0,
                            falloff_damage=[(1.0, 0.0), (0.5, 500.0)])


class ProjectileShotgunSmall(Projectile):

    def __init__(self) -> None:
        Projectile.__init__(self, sprite_url=get_absolute_resource_path("\\sprites\\tmp_projectile4.png"),
                            damage=8.0,
                            acceleration=-200.0,
                            falloff_damage=[(1.0, 0.0), (0.5, 500.0)])


class WeaponShotgun(Weapon):

    def __init__(self) -> None:
        super(WeaponShotgun, self).__init__(GunShotgun(), GunShotgunAlt())


if __name__ == '__main__':
    pass
