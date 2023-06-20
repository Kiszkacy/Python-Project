from typing import List, Tuple

from src.game.main.weapons.aura.aura import WeaponAura
from src.game.main.weapons.flamethrower.flamethrower import WeaponFlamethrower
from src.game.main.weapons.shotgun.shotgun import WeaponShotgun
from src.game.main.weapons.sinus.sinus import WeaponSinus
from src.game.main.weapons.sniper.sniper import WeaponSniper
from src.game.main.weapons.weapon import Weapon
from src.game.main.weapons.weird.weird import WeaponWeird


def calculate_level(exp: int) -> int:
    level_cost: int = 25
    level: int = 0
    while exp >= level_cost:
        exp -= level_cost
        level_cost += 25
        level += 1
    return level + 1


WeaponUnlocks: List[Tuple[Weapon, int]] = [
    (WeaponShotgun(), 3),
    (WeaponSniper(), 2),
    (WeaponSinus(), 1),
    (WeaponWeird(), 2),
    (WeaponFlamethrower(), 3),
    (WeaponAura(), 1)
]


def weapon_unlocks_for(level: int) -> List[Weapon]:
    return [weapon for weapon, min_lvl in WeaponUnlocks if min_lvl <= level]


if __name__ == '__main__':
    pass
