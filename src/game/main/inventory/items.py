from enum import IntEnum, auto
from typing import Dict, Optional


class Item(IntEnum):
    SCRAP = 0
    LARGE_SCRAP = auto()
    ENGINE_PART = auto()
    TOXIC_WASTE = auto()
    SMALL_DATA_CHIP = auto()
    MEDIUM_DATA_CHIP = auto()
    LARGE_DATA_CHIP = auto()
    GOLD_ORE = auto()
    IRON_ORE = auto()
    ALUMINIUM_ORE = auto()

# pseudo-fake class-dict something
ItemSize: Dict[Item, float] = {
    Item.SCRAP:             0.5,
    Item.LARGE_SCRAP:       2.0,
    Item.ENGINE_PART:       5.0,
    Item.TOXIC_WASTE:       1.0,
    Item.SMALL_DATA_CHIP:   5.0,
    Item.MEDIUM_DATA_CHIP:  10.0,
    Item.LARGE_DATA_CHIP:   20.0,
    Item.GOLD_ORE:          0.5,
    Item.IRON_ORE:          1.0,
    Item.ALUMINIUM_ORE:     0.5,
}


def get_item_size(item: Item) -> Optional[float]:
    return ItemSize.get(item, None)


if __name__ == '__main__':
    pass
