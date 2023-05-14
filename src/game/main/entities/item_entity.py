import arcade
import numpy as np

from src.game.main.entities.collidable_entity import CollidableEntity
from src.game.main.entities.entity import Entity
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.interfaces.collidable import Collidable
from src.game.main.inventory.items import Item
from src.game.main.util.math import magnitude
from src.game.main.util.path_loader import get_absolute_resource_path


class ItemEntity(CollidableEntity):

    ROTATION_SPEED_RATIO: float = 100.0
    ROTATION_SPEED: float = 5.0  # in deg

    def __init__(self, item_type: Item, starting_velocity: arcade.Vector, starting_position: arcade.Point) -> None:
        CollidableEntity.__init__(self, sprite_url=get_absolute_resource_path(f"\\sprites\\items\\{item_type.name.lower()}.png"),
                                  mass=10.0,
                                  belongs_to=ObjectCategory.ITEMS, collides_with=[ObjectCategory.PLAYER, ObjectCategory.ENEMIES, ObjectCategory.MISC, ObjectCategory.ITEMS])
        self.velocity = starting_velocity
        self.angle_rot: float = (magnitude(starting_velocity) / ItemEntity.ROTATION_SPEED_RATIO) * ItemEntity.ROTATION_SPEED
        self.angle_dir: float = np.random.randint(0, 2) * 2 - 1  # -1 or 1
        self.position = starting_position

    def on_update(self, delta_time: float = 1 / 60) -> None:
        super(ItemEntity, self).on_update(delta_time)
        # rotate
        self.angle += self.angle_rot * self.angle_dir

    def handle_collisions(self, delta: float) -> list[Collidable]:
        collisions: list[Collidable] = super(ItemEntity, self).handle_collisions(delta)

        if collisions: # update rotation param
            self.angle_rot = (magnitude(self.velocity) / ItemEntity.ROTATION_SPEED_RATIO) * ItemEntity.ROTATION_SPEED
            self.angle_dir: float = np.random.randint(0, 2) * 2 - 1 # -1 or 1

        return collisions


if __name__ == '__main__':
    pass
