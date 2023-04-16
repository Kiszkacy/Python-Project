
import arcade

from src.game.main.behaviors.behavior import Behavior
from src.game.main.entities.ship import Ship
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.util.path_loader import get_absolute_resource_path
from src.game.main.weapons.basic.basic import WeaponBasic


class EnemyShip(Ship): # TODO

    def __init__(self, starting_position: arcade.Point, weapons=None, behavior: Behavior = None) -> None:
        if weapons is None:
            weapons = [WeaponBasic()]

        super().__init__(sprite_url=get_absolute_resource_path("\\sprites\\tmp_ship0.png"),
                         weapons=weapons,
                         weapon_count=len(weapons),
                         belongs_to=ObjectCategory.ENEMIES,
                         collides_with=[ObjectCategory.STATIC, ObjectCategory.PLAYER, ObjectCategory.PROJECTILES],
                         deceleration=600,
                         mass=50)

        self.position = starting_position
        self.behavior = behavior


    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.behavior.execute(delta_time)
        super().on_update()


    def add_behavior(self, behavior: Behavior):
        self.behavior = behavior


if __name__ == '__main__':
    pass
