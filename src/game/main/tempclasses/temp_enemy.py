
import arcade
import numpy as np

from src.game.main.entities.ship import Ship
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.interfaces.launchable import Launchable
from src.game.main.util.path_loader import get_absolute_resource_path
from src.game.main.weapons.shotgun.shotgun import WeaponShotgun


class TempEnemy(Ship, Launchable):

    def __init__(self) -> None:
        super().__init__(sprite_url=get_absolute_resource_path("\\sprites\\ships\\small_002.png"),
                         weapons=[WeaponShotgun()],
                         mass=10.0,
                         weapon_count=1,
                         belongs_to=ObjectCategory.ENEMIES,
                         collides_with=[ObjectCategory.STATIC, ObjectCategory.PLAYER, ObjectCategory.PROJECTILES, ObjectCategory.ENEMIES],
                         hp_max=50.0, shd_max=0.0)


    def launch(self, from_: arcade.Point, angle: float, speed: float) -> None:
        direction: arcade.Vector = (np.cos(np.deg2rad(angle)), np.sin(np.deg2rad(angle))) # already normalized
        self.position = (from_[0] + direction[0] * 50.0, from_[1] + direction[1] * 50.0)
        self.angle = angle
        self.velocity = (direction[0] * speed, direction[1] * speed)


if __name__ == '__main__':
    pass
