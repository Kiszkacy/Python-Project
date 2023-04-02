
from src.weapons.Weapon import Weapon
from src.weapons.weird.GunWeird import GunWeird


class WeaponWeird(Weapon):

    def __init__(self) -> None:
        super(WeaponWeird, self).__init__(GunWeird())


if __name__ == '__main__':
    pass
