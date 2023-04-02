
from src.weapons.Weapon import Weapon
from src.weapons.aura.GunAura import GunAura


class WeaponAura(Weapon):

    def __init__(self) -> None:
        super(WeaponAura, self).__init__(GunAura())


if __name__ == '__main__':
    pass
