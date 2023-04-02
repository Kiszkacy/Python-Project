
from src.weapons.LaunchableGun import LaunchableGun
from src.weapons.aura.ProjectileAura import ProjectileAura


class GunAura(LaunchableGun):

    def __init__(self) -> None:
        super().__init__(launchable=ProjectileAura(),
                         barrel_count=16,
                         even_spread=360.0,
                         launch_spread=2.0,
                         launch_speed=100.0)


if __name__ == '__main__':
    pass
