
from src.weapons.LaunchableGun import LaunchableGun
from src.weapons.sinus.ProjectileSinus import ProjectileSinus


class GunSinus(LaunchableGun):

    def __init__(self) -> None:
        super().__init__(launchable=ProjectileSinus(), shot_spread=0.0)


if __name__ == '__main__':
    pass
