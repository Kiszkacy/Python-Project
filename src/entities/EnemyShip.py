
import arcade
from src.entities.Ship import Ship
from src.auxilary.ObjectCategory import ObjectCategory
from src.behaviors.behavior import Behavior
from src.weapons.basic.WeaponBasic import WeaponBasic


class EnemyShip(Ship): # TODO

    def __init__(self, starting_position: arcade.Point, weapons=None, behavior: Behavior = None) -> None:
        if weapons is None:
            weapons = [WeaponBasic(ObjectCategory.ENEMIES)]

        super().__init__(sprite_url="..\\resources\\sprites\\tmp_ship1.png",
                         weapons=weapons,
                         weapon_count=len(weapons),
                         belongs_to=ObjectCategory.ENEMIES,
                         collides_with=[ObjectCategory.STATIC, ObjectCategory.PLAYER, ObjectCategory.PROJECTILES],
                         deceleration=600)

        self.position = starting_position
        self.behavior = behavior


    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.behavior.execute(delta_time)
        super().on_update()


    def add_behavior(self, behavior: Behavior):
        self.behavior = behavior


if __name__ == '__main__':
    pass
