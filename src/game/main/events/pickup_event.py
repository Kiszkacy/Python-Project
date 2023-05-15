
from dataclasses import dataclass

from src.game.main.events.event import Event
from src.game.main.inventory.inventory import Inventory
from src.game.main.inventory.items import Item


@dataclass
class PickupEvent(Event):
    picked: Item
    into: Inventory


if __name__ == '__main__':
    pass
