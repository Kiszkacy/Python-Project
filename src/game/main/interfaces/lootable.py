import arcade
import numpy as np

from src.game.main.entities.item_entity import ItemEntity
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.lootdrop.lootdrop import LootDrop
from src.game.main.singletons.entity_handler import EntityHandler


class Lootable:

    def drop(self, lootdrop: LootDrop, at: arcade.Point) -> None:
        for item in lootdrop.calc():
            EntityHandler.add(ItemEntity(item, # TODO this shouldnt be hardcoded
                                starting_position=(at[0] + np.random.randint(-32, 32), at[1] + np.random.randint(-32, 32)),
                                starting_velocity=(np.random.randint(-9, 9), np.random.randint(-9, 9))), ObjectCategory.ITEMS)


if __name__ == '__main__':
    pass
