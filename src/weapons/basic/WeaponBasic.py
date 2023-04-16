
from src.weapons.Weapon import Weapon
from src.weapons.basic.GunBasic import GunBasic
from src.weapons.basic.GunBasicAlt import GunBasicAlt
from src.auxilary.ObjectCategory import ObjectCategory


class WeaponBasic(Weapon):

    def __init__(self, owner: ObjectCategory) -> None:
        super(WeaponBasic, self).__init__(GunBasic(owner), GunBasicAlt())


if __name__ == '__main__':
    pass
