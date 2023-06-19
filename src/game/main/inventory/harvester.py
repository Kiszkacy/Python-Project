from typing import List

import arcade

from src.game.main.entities.collidable_entity import CollidableEntity
from src.game.main.entities.entity import Entity
from src.game.main.entities.item_entity import ItemEntity
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.events.pickup_event import PickupEvent
from src.game.main.interfaces.collidable import Collidable
from src.game.main.inventory.inventory import Inventory
from src.game.main.singletons.entity_handler import EntityHandler
from src.game.main.singletons.event_register import EventRegister
from src.game.main.util.math import normalize
from src.game.main.util.path_loader import get_absolute_resource_path


class Harvester(Entity):

    def __init__(self, target_inventory: Inventory, range: float = 256.0, pickup_range: float = 48.0, strength: float = 256.0) -> None:
        # error sprite size: 256x256
        super(Harvester, self).__init__(sprite_url=get_absolute_resource_path("\\sprites\\error.png"))
        self.inventory: Inventory = target_inventory
        self.range: float = range
        self.pickup_range: float = pickup_range
        self.strength: float = strength
        self.active: bool = True

    def on_update(self, delta_time: float = 1 / 60) -> None:
        self.look_for_items(delta_time)

    # THIS MUST BE CALLED BY THE PARENT CLASS TO WORK PROPERLY
    def update_position(self, position: arcade.Point) -> None:
        self.position = position

    def look_for_items(self, delta: float) -> None:
        if not self.active: return
        # NOTE: if everything works correctly we are 100% sure that colliders are of ItemEntity type
        for obj in EntityHandler.categorized[ObjectCategory.ITEMS]: # TODO change to buckets !!! VERY IMPORTANT
            item: ItemEntity = obj
            dist: float = arcade.get_distance_between_sprites(self, item)
            if dist <= self.pickup_range: # pickup item
                if self.inventory.append(item.type, 1):
                    EventRegister.register_new(PickupEvent(item.type, self.inventory))
                    item.destroy()
                print(self.inventory.items, f"{self.inventory.capacity}/{self.inventory.max_capacity}")
            if dist <= self.range: # move item closer to itself
                direction: arcade.Point = (self.position[0] - obj.position[0], self.position[1] - obj.position[1])
                direction = normalize(direction)
                push: arcade.Point = (direction[0]*self.strength*delta, direction[1]*self.strength*delta)
                obj.velocity = (push[0] + obj.velocity[0], push[1] + obj.velocity[1])

    def set_active(self, to: bool) -> None:
        self.active = to


if __name__ == '__main__':
    pass
