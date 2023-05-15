from typing import Dict, Tuple, List

from src.game.main.inventory.items import Item, get_item_size
from src.game.main.util.dotdict import dotdict


class Inventory:

    def __init__(self, capacity: float) -> None:
        self.max_capacity: float = capacity
        self.capacity: float = 0.0
        self.items: Dict[Item, int] = dotdict()


    def append(self, item: Item, count: int = 1) -> bool:
        if get_item_size(item) and get_item_size(item)*count + self.capacity <= self.max_capacity:
            self.items[item] = self.items.get(item, 0) + count
            self.capacity += get_item_size(item)*count
            return True
        return False


    def extend(self, items: List[Tuple[Item, int]]) -> bool:
        total_capacity: float = 0.0
        for item, count in items:
            if not get_item_size(item): return False # item not found
            total_capacity += get_item_size(item)*count

        if self.capacity + total_capacity <= self.max_capacity: return False
        # else
        self.capacity += total_capacity
        for item, count in items:
            self.items[item] = self.items.get(item, 0) + count
        return True


    def delete(self, item: Item, count: int = 1) -> bool:
        # if item not in eq or less than to delete
        if not self.items.get(item) or self.items.get(item) < count: return False
        self.items.item = self.items.get(item) - count
        self.capacity -= get_item_size(item)*count
        return True


    def delete_from(self, items: List[Tuple[Item, int]]) -> bool:
        # TODO implement
        raise RuntimeError("NOT IMPLEMENTED")
        return True


    def clear(self) -> None:
        self.items = dotdict()
        self.capacity = 0.0


if __name__ == '__main__':
    pass
