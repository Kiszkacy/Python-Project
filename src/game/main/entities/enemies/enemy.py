from typing import List, Callable

import arcade

from src.game.main.behaviors.behavior import Behavior
from src.game.main.behaviors.enemy_behavior_creator import basic_enemy_behavior
from src.game.main.entities.ship import Ship
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.interfaces.destroyable import Destroyable
from src.game.main.interfaces.lootable import Lootable
from src.game.main.util.path_loader import get_absolute_resource_path
from src.game.main.weapons.enemy.basic.basic import WeaponBasic
from src.game.main.weapons.weapon import Weapon


class Enemy(Ship, Lootable):

    # LOOT_TABLE: LootDrop = LootDropLoader.load_from_json(get_absolute_resource_path("\\loottables\\basic.json"))

    def __init__(self, starting_position: arcade.Point, behavior_creator: Callable = basic_enemy_behavior,
                 sprite_url: str = get_absolute_resource_path("\\sprites\\ships\\small_002.png"),
                 mass: float = 50.0,
                 hp_max: float = 30.0, shd_max: float = 10.0, power_max: float = 10000.0,
                 power_regen_amount: float = 1000.0,
                 power_regen_delay: float = 0.0, rotation_speed: float = 180.0, max_speed: float = 400.0,
                 acceleration: float = 350.0, deceleration: float = 500.0, weapons: list[Weapon] = None) -> None:

        if weapons is None: weapons = [WeaponBasic()] # default
        super().__init__(sprite_url=sprite_url,
                         mass=mass, hp_max=hp_max, shd_max=shd_max, power_max=power_max, power_regen_amount=power_regen_amount,
                         power_regen_delay=power_regen_delay, rotation_speed=rotation_speed, max_speed=max_speed,
                         acceleration=acceleration, deceleration=deceleration,
                         weapons=weapons,
                         weapon_count=len(weapons),
                         belongs_to=ObjectCategory.ENEMIES,
                         collides_with=[ObjectCategory.STATIC, ObjectCategory.PLAYER, ObjectCategory.PROJECTILES, ObjectCategory.ENEMIES])

        self.position = starting_position
        self.behavior: Behavior = behavior_creator(self)
        self.behavior_creator = behavior_creator

    # NOTE are we doing this twice ?
    def initialize(self):
        self.behavior = self.behavior_creator(self)

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.behavior.execute(delta_time)
        super().on_update()

    def add_behavior(self, behavior: Behavior):
        self.behavior = behavior

    # TODO add default lootdrop on destroy with "error items"
    # def destroy(self) -> Destroyable:


if __name__ == '__main__':
    pass
