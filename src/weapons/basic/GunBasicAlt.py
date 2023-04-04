
from src.tempclasses.tempEnemy import TempEnemy
from src.weapons.LaunchableGun import LaunchableGun


class GunBasicAlt(LaunchableGun):

    def __init__(self) -> None:
        super().__init__(launchable=TempEnemy(),
                         launch_speed=200.0,
                         shots_per_sec=3.0,
                         power_cost=7.0)


if __name__ == '__main__':
    pass
