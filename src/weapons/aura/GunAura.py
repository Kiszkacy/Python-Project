
from src.weapons.LaunchableGun import LaunchableGun
from src.weapons.aura.ProjectileAura import ProjectileAura


class GunAura(LaunchableGun):

    def __init__(self) -> None:
        super().__init__(launchable=ProjectileAura(),
                         barrel_count=16,
                         even_spread=360.0,
                         launch_spread=0.0,
                         launch_speed=100.0,
                         shot_spread=25.0,
                         power_cost=1.0)


if __name__ == '__main__':
    pass
