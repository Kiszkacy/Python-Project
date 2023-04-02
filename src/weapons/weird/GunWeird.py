
from src.weapons.LaunchableGun import LaunchableGun
from src.weapons.weird.ProjectileWeird import ProjectileWeird


class GunWeird(LaunchableGun):

    def __init__(self) -> None:
        super().__init__(launchable=ProjectileWeird(),
                         shot_spread=0.0,
                         launch_spread=10.0,
                         barrel_count=6,
                         barrels_even_offset=0.0, # TODO FIX ME
                         custom_spread=[-45.0, -30.0, 0.0, 30.0, 45.0, -180.0],
                         shots_per_sec=6.0,
                         launch_speed=600.0)


if __name__ == '__main__':
    pass
