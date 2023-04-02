
from src.weapons.Weapon import Weapon
from src.weapons.shotgun.GunShotgun import GunShotgun
from src.weapons.shotgun.GunShotgunAlt import GunShotgunAlt


class WeaponShotgun(Weapon):

    def __init__(self) -> None:
        super(WeaponShotgun, self).__init__(GunShotgun(), GunShotgunAlt())


if __name__ == '__main__':
    pass
