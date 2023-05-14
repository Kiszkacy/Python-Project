import arcade

from src.game.main.behaviors.behavior import Behavior
from src.game.main.behaviors.enemy_behavior_creator import basic_enemy_behavior
from src.game.main.entities.ship import Ship
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.util.path_loader import get_absolute_resource_path
from src.game.main.weapons.enemy.basic.basic import WeaponBasic


class EnemyShip(Ship): # TODO

    def __init__(self, starting_position: arcade.Point, weapons=None, behavior_creator: callable = basic_enemy_behavior) -> None:
        if weapons is None:
            weapons = [WeaponBasic()]

        super().__init__(sprite_url=get_absolute_resource_path("\\sprites\\ships\\small_002.png"),
                         weapons=weapons,
                         weapon_count=len(weapons),
                         belongs_to=ObjectCategory.ENEMIES,
                         collides_with=[ObjectCategory.STATIC, ObjectCategory.PLAYER, ObjectCategory.PROJECTILES, ObjectCategory.ENEMIES],
                         deceleration=600,
                         mass=50)

        self.position = starting_position
        self.behavior = behavior_creator(self)
        self.behavior_creator = behavior_creator

    def initialize(self):
        self.behavior = self.behavior_creator(self)

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.behavior.execute(delta_time)
        super().on_update()


    def add_behavior(self, behavior: Behavior):
        self.behavior = behavior


if __name__ == '__main__':
    pass
