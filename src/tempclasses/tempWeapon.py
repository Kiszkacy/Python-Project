
from src.tempclasses.tempGun import TempGun
from src.weapons.Weapon import Weapon


class TempWeapon(Weapon):

    def __init__(self) -> None:
        super().__init__(TempGun())


if __name__ == '__main__':
    pass
