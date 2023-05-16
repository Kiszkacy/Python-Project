import arcade

from src.game.main.entities.enemies.enemy import Enemy
from src.game.main.interfaces.destroyable import Destroyable
from src.game.main.lootdrop.loader import Loader as LootDropLoader
from src.game.main.lootdrop.lootdrop import LootDrop
from src.game.main.util.path_loader import get_absolute_resource_path
from src.game.main.weapons.enemy.basic.basic import WeaponBasic
from src.game.main.weapons.enemy.torpedovolley.torpedovolley import WeaponTorpedoVolley


class EnemySpecial(Enemy):

    LOOT_TABLE: LootDrop = LootDropLoader.load_from_json(get_absolute_resource_path("\\loottables\\enemies\\special.json"))

    def __init__(self, starting_position: arcade.Point) -> None:
        super().__init__(starting_position, sprite_url=get_absolute_resource_path("\\sprites\\ships\\medium_002.png"),
                         weapons=[WeaponTorpedoVolley()],
                         acceleration=300.0, max_speed=350.0, deceleration=400.0, hp_max=75.0, shd_max=50.0, rotation_speed=120.0)

    def destroy(self) -> Destroyable:
        self.drop(EnemySpecial.LOOT_TABLE, self.position)
        return super(EnemySpecial, self).destroy()


if __name__ == '__main__':
    pass
