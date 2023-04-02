
from src.weapons.Weapon import Weapon
from src.weapons.sinus.GunSinus import GunSinus


class WeaponSinus(Weapon):

    def __init__(self) -> None:
        super(WeaponSinus, self).__init__(GunSinus())


if __name__ == '__main__':
    pass
