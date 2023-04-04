
from src.weapons.Weapon import Weapon
from src.weapons.basic.GunBasic import GunBasic
from src.weapons.basic.GunBasicAlt import GunBasicAlt


class WeaponBasic(Weapon):

    def __init__(self) -> None:
        super(WeaponBasic, self).__init__(GunBasic(), GunBasicAlt())


if __name__ == '__main__':
    pass
