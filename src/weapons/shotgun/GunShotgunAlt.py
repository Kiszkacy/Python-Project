
from src.weapons.LaunchableGun import LaunchableGun
from src.weapons.shotgun.ProjectileShotgunAlt import ProjectileShotgunAlt


class GunShotgunAlt(LaunchableGun):

    def __init__(self) -> None:
        super().__init__(
            power_cost=4.0,
            barrel_count=3,
            barrels_even_offset=0.0, #45.0 TODO FIX BUG
            launch_speed=700.0,
            launch_spread=1.0,
            shot_spread=5.0,
            even_spread=12.0,
            shots_per_sec=4.0,
            launchable=ProjectileShotgunAlt())


if __name__ == '__main__':
    pass
