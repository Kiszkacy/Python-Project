
from src.weapons.LaunchableGun import LaunchableGun
from src.weapons.basic.ProjectileBasic import ProjectileBasic
from src.weapons.basic.enemy_projectile_basic import EnemyProjectileBasic
from src.auxilary.ObjectCategory import ObjectCategory


class GunBasic(LaunchableGun):

    def __init__(self, owner: ObjectCategory) -> None:
        if owner == ObjectCategory.PLAYER:
            super().__init__(launchable=ProjectileBasic())
        else:
            super().__init__(launchable=EnemyProjectileBasic())


if __name__ == '__main__':
    pass
