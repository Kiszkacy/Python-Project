
import arcade
from src.interfaces.Launchable import Launchable
from src.weapons.LaunchableGun import LaunchableGun
from src.weapons.shotgun.ProjectileShotgunBig import ProjectileShotgunBig
from src.weapons.shotgun.ProjectileShotgunSmall import ProjectileShotgunSmall


class GunShotgun(LaunchableGun):

    def __init__(self) -> None:
        self.launchables: list[Launchable] = [ProjectileShotgunSmall(), ProjectileShotgunBig()]
        self.launchable_idx: int = 0
        super().__init__(
            power_cost=7.0,
            barrel_count=6,
            barrels_even_offset=0.0,
            launch_speed=700.0,
            launch_spread=5.0,
            shot_spread=10.0,
            even_spread=35.0,
            shots_per_sec=2.0,
            launchable=self.launchables[self.launchable_idx])


    def launch(self, from_: arcade.Point, angle: float, pos_offset: arcade.Vector, idx: int) -> None:
        super(GunShotgun, self).launch(from_, angle, pos_offset, idx)
        self.launchable_idx = (self.launchable_idx+1) % len(self.launchables)
        self.launchable = self.launchables[self.launchable_idx]


if __name__ == '__main__':
    pass
