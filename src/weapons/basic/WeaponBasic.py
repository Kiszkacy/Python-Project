
from src.weapons.Weapon import Weapon
from src.weapons.basic.GunBasic import GunBasic


class WeaponBasic(Weapon):

    def __init__(self) -> None:
        super(WeaponBasic, self).__init__(GunBasic())


if __name__ == '__main__':
    pass
