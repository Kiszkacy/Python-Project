
from src.tempclasses.tempProjectile import TempProjectile
from src.weapons.LaunchableGun import LaunchableGun


class TempGun(LaunchableGun):

    def __init__(self) -> None:
        super().__init__(launchable=TempProjectile())


# def __init__(self, damage: float = 3.0, power_cost: float = 2.0, barrel_count: int = 1,
    #              barrels: list[arcade.Point] = None, barrels_even_offset: float = 3.0, launch_speed: float = 300.0,
    #              launch_spread: float = 0.0, shot_spread: float = 5.0, even_spread: float = 0.0,
    #              shots_per_sec: float = 3.0, launchable: Launchable = Projectile()) -> None:
    #     super().__init__(damage, power_cost, barrel_count, barrels, barrels_even_offset)
    #     # launchableGun stats
    #     self.launch_speed: float = launch_speed
    #     self.launch_spread: float = launch_spread
    #     self.shot_spread: float = shot_spread
    #     self.even_spread: float = even_spread
    #     self.shots_per_sec: float = shots_per_sec
    #     self.launchable: Launchable = launchable


if __name__ == '__main__':
    pass
