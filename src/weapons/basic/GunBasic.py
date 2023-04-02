
from src.weapons.LaunchableGun import LaunchableGun
from src.weapons.basic.ProjectileBasic import ProjectileBasic


class GunBasic(LaunchableGun):

    def __init__(self) -> None:
        super().__init__(launchable=ProjectileBasic())


if __name__ == '__main__':
    pass
