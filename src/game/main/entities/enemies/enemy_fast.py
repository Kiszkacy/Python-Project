import arcade

from src.game.main.entities.enemies.enemy import Enemy
from src.game.main.interfaces.destroyable import Destroyable
from src.game.main.lootdrop.loader import Loader as LootDropLoader
from src.game.main.lootdrop.lootdrop import LootDrop
from src.game.main.util.math import magnitude
from src.game.main.util.path_loader import get_absolute_resource_path
from src.game.main.weapons.enemy.basic.basic import WeaponBasic


class EnemyFast(Enemy):

    LOOT_TABLE: LootDrop = LootDropLoader.load_from_json(get_absolute_resource_path("\\loottables\\enemies\\fast.json"))

    def __init__(self, starting_position: arcade.Point) -> None:
        super().__init__(starting_position, sprite_url=get_absolute_resource_path("\\sprites\\ships\\small_001.png"),
                         weapons=[WeaponBasic()],
                         acceleration=650.0, max_speed=550.0, deceleration=800.0, hp_max=25.0, shd_max=25.0, rotation_speed=360.0)

    def destroy(self) -> Destroyable:
        self.drop(EnemyFast.LOOT_TABLE, self.position)
        return super(EnemyFast, self).destroy()


if __name__ == '__main__':
    pass
