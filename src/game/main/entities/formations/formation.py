from typing import List, Tuple, Optional

import arcade

from src.game.main.entities.entity import Entity
from src.game.main.enums.object_category import ObjectCategory
from src.game.main.singletons.entity_handler import EntityHandler


class Formation:

    def __init__(self, width: int, height: int, entities: Optional[List[Tuple[Entity, arcade.Point]]] = None) -> None:
        self.width: int = width
        self.height: int = height
        self.entities: List[Tuple[Entity, arcade.Point]] = [] if entities is None else entities

    def add_entity(self, entity: Entity, offset: arcade.Point) -> None:
        self.entities.append((entity, offset))

    def place(self, at: arcade.Point, layer: ObjectCategory, bucketable: bool = False) -> None:
        for e, offset in self.entities:
            e.position = (at[0]+offset[0], at[1]+offset[1])
            print(e.position)
            EntityHandler.add(e, layer, bucketable)


if __name__ == '__main__':
    pass
