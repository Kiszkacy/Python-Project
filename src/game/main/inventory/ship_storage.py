from typing import Tuple

import numpy as np

from src.game.main.entities.entity import Entity
from src.game.main.entities.item_entity import ItemEntity
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.inventory.harvester import Harvester
from src.game.main.inventory.inventory import Inventory
from src.game.main.inventory.items import Item
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.util.path_loader import get_absolute_resource_path


class ShipStorage(Entity):

    HARVESTER_INACTIVE_FOR: float = 3.0 # TODO constant
    TRASH_ITEMS: Tuple[Item] = (Item.SCRAP, Item.LARGE_SCRAP, Item.ENGINE_PART, Item.TOXIC_WASTE)

    def __init__(self, inventory_size: float = 200.0, harvester_traction_range: float = 256.0,
                 harvester_pickup_range: float = 48.0) -> None:
        super(ShipStorage, self).__init__(sprite_url=get_absolute_resource_path("\\sprites\\error.png"))
        self.inventory: Inventory = Inventory(inventory_size)
        self.harvester: Harvester = Harvester(self.inventory, harvester_traction_range, harvester_pickup_range)
        self.harvester_inactive_timer: float = 0.0

    def drop_all_items(self) -> None:
        self.harvester.active = False
        self.harvester_inactive_timer = ShipStorage.HARVESTER_INACTIVE_FOR
        for item in Item:
            while self.inventory.delete(item, 1):
                EntityHandler.add(ItemEntity(item,
                                             starting_position=self.position,
                                             starting_velocity=(np.random.randint(-120, 120), np.random.randint(-120, 120))),
                                  ObjectCategory.ITEMS, True)

    def drop_trash(self) -> None:
        self.harvester.active = False
        self.harvester_inactive_timer = ShipStorage.HARVESTER_INACTIVE_FOR
        for item in ShipStorage.TRASH_ITEMS:
            while self.inventory.delete(item, 1):
                print(self.inventory.items)
                EntityHandler.add(ItemEntity(item,
                                             starting_position=self.position,
                                             starting_velocity=(np.random.randint(-120, 120), np.random.randint(-120, 120))),
                                  ObjectCategory.ITEMS, True)


    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.harvester.on_update(delta_time)
        self.harvester.update_position(self.position)

        if self.harvester_inactive_timer > 0.0:
            self.harvester_inactive_timer -= delta_time
            if self.harvester_inactive_timer <= 0.0: self.harvester.active = True


if __name__ == '__main__':
    pass
