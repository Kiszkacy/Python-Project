from __future__ import annotations
from typing import List, Callable

from src.game.main.inventory.items import Item


class LootDrop:

    def __init__(self, entries: List[Item|LootDrop], rolls: Callable, chance: Callable) -> None:
        self.rolls: Callable = rolls
        self.entries: List[Item|LootDrop] = entries
        self.chance: Callable = chance

    def calc(self) -> List[Item]:
        result: List[Item] = []
        for i in range(self.rolls()):
            picked: List[int] = self.chance() # list of indexes of picked entries

            for j in range(len(picked)):
                if isinstance(self.entries[picked[j]], LootDrop):
                    loot: LootDrop = self.entries[picked[j]]
                    result.extend(loot.calc())
                else: # Item
                    result.append(self.entries[picked[j]])

        return result


if __name__ == '__main__':
    pass
