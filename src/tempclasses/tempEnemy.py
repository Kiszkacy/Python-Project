
import arcade
import numpy as np
from src.entities.Ship import Ship
from src.interfaces.Launchable import Launchable
from src.weapons.shotgun.WeaponShotgun import WeaponShotgun
from src.auxilary.ObjectCategory import ObjectCategory


class TempEnemy(Ship, Launchable):

    def __init__(self) -> None:
        super().__init__(sprite_url="..\\resources\\sprites\\tmp_ship1.png",
                         weapons=[WeaponShotgun()],
                         weapon_count=1,
                         belongs_to=ObjectCategory.ENEMIES,
                         collides_with=[ObjectCategory.STATIC, ObjectCategory.PLAYER, ObjectCategory.PROJECTILES, ObjectCategory.ENEMIES],
                         max_hp=50.0, max_shd=0.0)


    def launch(self, from_: arcade.Point, angle: float, speed: float) -> None:
        direction: arcade.Vector = (np.cos(np.deg2rad(angle)), np.sin(np.deg2rad(angle))) # already normalized
        self.position = (from_[0] + direction[0] * 50.0, from_[1] + direction[1] * 50.0)
        self.angle = angle
        self.velocity = (direction[0] * speed, direction[1] * speed)


if __name__ == '__main__':
    pass
